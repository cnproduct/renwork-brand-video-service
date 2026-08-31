#!/usr/bin/env python3
"""Create, scan, update, and validate a resumable video artifact manifest."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


SCENE_STATES = {
    "planned",
    "prompted",
    "generating",
    "generated",
    "technically_verified",
    "needs_revision",
    "accepted",
    "blocked",
}
GATE_STATES = {"pending", "pass", "fail", "waived"}
GATE_NAMES = (
    "technical_playback",
    "scene_content_match",
    "picture_subtitle_audio_sync",
    "no_duplicate_footage",
    "brand_consistency",
    "cover_applied",
    "human_review",
)
DEFAULT_GLOBS = (
    "scene*.mp4",
    "*composite*.mp4",
    "*final*.mp4",
    "*cover*.png",
    "*cover*.jpg",
    "*cover*.jpeg",
    "*copy*.md",
    "voice*.mp3",
    "voice*.wav",
    "produce*.py",
    "composite*.py",
    "generate_cover.py",
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_manifest(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid manifest JSON at {path}: {exc}") from exc
    if data.get("schema_version") != "1.0":
        raise SystemExit(f"Unsupported schema_version: {data.get('schema_version')!r}")
    return data


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def project_root(data: dict) -> Path:
    return Path(data["project"]["root"]).expanduser().resolve()


def ensure_within(root: Path, candidate: Path) -> Path:
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise SystemExit(f"Path escapes project root: {candidate}")
    return resolved


def relative_artifact(root: Path, value: str) -> str:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return ensure_within(root, candidate).relative_to(root).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe_media(path: Path) -> dict | None:
    if shutil.which("ffprobe") is None:
        return None
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"probe_error": result.stderr.strip() or f"ffprobe exit {result.returncode}"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"probe_error": "ffprobe returned invalid JSON"}
    fmt = payload.get("format", {})
    duration = fmt.get("duration")
    return {
        "duration_seconds": round(float(duration), 3) if duration is not None else None,
        "format_name": fmt.get("format_name"),
        "streams": payload.get("streams", []),
    }


def classify(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if re.match(r"^scene\d+[_-].*\.mp4$", name):
        return "scene_video"
    if suffix == ".mp4" and "final" in name:
        return "final_video"
    if suffix == ".mp4" and ("composite" in name or "mashup" in name):
        return "composite_video"
    if suffix in {".png", ".jpg", ".jpeg"} and "cover" in name:
        return "cover"
    if suffix == ".md" and "copy" in name:
        return "channel_copy"
    if suffix in {".mp3", ".wav", ".m4a", ".aac"}:
        return "audio"
    if suffix == ".py":
        return "production_script"
    return "other"


def artifact_record(root: Path, path: Path, previous: dict | None = None) -> dict:
    stat = path.stat()
    record = {
        "path": path.relative_to(root).as_posix(),
        "role": classify(path),
        "bytes": stat.st_size,
        "modified_at": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "sha256": sha256_file(path),
    }
    if path.suffix.lower() in {".mp4", ".mov", ".mkv", ".mp3", ".wav", ".m4a", ".aac"}:
        record["media"] = probe_media(path)
    if previous and "review" in previous:
        record["review"] = previous["review"]
    return record


def append_history(data: dict, action: str, details: dict) -> None:
    data.setdefault("history", []).append(
        {"timestamp": utc_now(), "action": action, "details": details}
    )
    data["project"]["updated_at"] = utc_now()


def parse_scene(value: str) -> dict:
    parts = value.split(":", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("scene must be ORDER:SLUG:TITLE")
    order_text, slug, title = (part.strip() for part in parts)
    try:
        order = int(order_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("scene order must be an integer") from exc
    if order < 1 or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug):
        raise argparse.ArgumentTypeError("scene slug must use lowercase letters, digits, _ or -")
    if not title:
        raise argparse.ArgumentTypeError("scene title cannot be empty")
    return {
        "scene_id": f"scene{order}",
        "order": order,
        "slug": slug,
        "title": title,
        "expected_path": f"scene{order}_{slug}.mp4",
        "status": "planned",
        "selected_artifact": None,
        "attempts": [],
        "review": {"technical": "pending", "content": "pending", "notes": []},
    }


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")
    manifest_path = root / args.filename
    if manifest_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing manifest: {manifest_path}")
    scenes = sorted(args.scene, key=lambda item: item["order"])
    ids = [item["scene_id"] for item in scenes]
    orders = [item["order"] for item in scenes]
    if len(ids) != len(set(ids)) or len(orders) != len(set(orders)):
        raise SystemExit("Scene orders must be unique")
    now = utc_now()
    data = {
        "schema_version": "1.0",
        "project": {
            "project_id": args.project_id,
            "root": str(root),
            "brand_profile_id": args.brand_profile_id,
            "brief_source": args.brief_source,
            "channel": args.channel,
            "aspect_ratio": args.aspect_ratio,
            "target_duration_seconds": args.target_duration,
            "created_at": now,
            "updated_at": now,
        },
        "scenes": scenes,
        "artifacts": [],
        "stages": {
            "planning": "complete",
            "scene_generation": "pending",
            "composition": "pending",
            "cover": "pending",
            "channel_copy": "pending",
            "technical_validation": "pending",
        },
        "acceptance_gates": {
            name: {
                "status": "pending",
                "evidence": None,
                "reviewer": None,
                "note": None,
                "updated_at": None,
            }
            for name in GATE_NAMES
        },
        "history": [{"timestamp": now, "action": "init", "details": {"scene_count": len(scenes)}}],
    }
    atomic_write(manifest_path, data)
    print(manifest_path)
    return 0


def discover_files(root: Path, globs: list[str]) -> list[Path]:
    found: set[Path] = set()
    for pattern in globs:
        if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
            raise SystemExit(f"Glob must stay below project root: {pattern}")
        for candidate in root.glob(pattern):
            if candidate.is_file():
                found.add(ensure_within(root, candidate))
    return sorted(found, key=lambda path: path.relative_to(root).as_posix())


def cmd_scan(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    data = load_manifest(manifest_path)
    root = project_root(data)
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")
    globs = list(DEFAULT_GLOBS) + list(args.glob or [])
    previous = {item["path"]: item for item in data.get("artifacts", [])}
    files = discover_files(root, globs)
    data["artifacts"] = [
        artifact_record(root, path, previous.get(path.relative_to(root).as_posix()))
        for path in files
    ]
    by_path = {item["path"]: item for item in data["artifacts"]}
    for scene in data["scenes"]:
        expected = scene["expected_path"]
        selected = scene.get("selected_artifact")
        candidate = selected if selected in by_path else expected if expected in by_path else None
        if candidate:
            scene["selected_artifact"] = candidate
            if scene["status"] in {"planned", "prompted", "generating", "blocked"}:
                scene["status"] = "generated"
    scene_states = [scene["status"] for scene in data["scenes"]]
    if scene_states and all(state in {"generated", "technically_verified", "needs_revision", "accepted"} for state in scene_states):
        data["stages"]["scene_generation"] = "complete"
    elif any(state != "planned" for state in scene_states):
        data["stages"]["scene_generation"] = "in_progress"
    roles = {item["role"] for item in data["artifacts"]}
    if roles & {"composite_video", "final_video"}:
        data["stages"]["composition"] = "generated"
    if "cover" in roles:
        data["stages"]["cover"] = "generated"
    if "channel_copy" in roles:
        data["stages"]["channel_copy"] = "generated"
    final_records = [item for item in data["artifacts"] if item["role"] == "final_video"]
    if final_records and all(not (item.get("media") or {}).get("probe_error") for item in final_records):
        data["stages"]["technical_validation"] = "media_parsed"
    append_history(data, "scan", {"artifact_count": len(data["artifacts"]), "globs": globs})
    atomic_write(manifest_path, data)
    print(json.dumps({"manifest": str(manifest_path), "artifacts": len(data["artifacts"])}, ensure_ascii=False))
    return 0


def find_scene(data: dict, scene_id: str) -> dict:
    for scene in data["scenes"]:
        if scene["scene_id"] == scene_id:
            return scene
    raise SystemExit(f"Unknown scene_id: {scene_id}")


def cmd_set_scene(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    data = load_manifest(manifest_path)
    root = project_root(data)
    scene = find_scene(data, args.scene_id)
    scene["status"] = args.status
    artifact = None
    if args.artifact:
        artifact = relative_artifact(root, args.artifact)
        artifact_path = root / artifact
        if not artifact_path.is_file() or artifact_path.stat().st_size == 0:
            raise SystemExit(f"Selected artifact is missing or empty: {artifact_path}")
        scene["selected_artifact"] = artifact
    if args.attempt_status:
        scene.setdefault("attempts", []).append(
            {
                "timestamp": utc_now(),
                "provider": args.provider,
                "status": args.attempt_status,
                "artifact": artifact,
                "note": args.note,
            }
        )
    if args.note:
        scene.setdefault("review", {}).setdefault("notes", []).append(
            {"timestamp": utc_now(), "text": args.note}
        )
    append_history(
        data,
        "set_scene",
        {"scene_id": args.scene_id, "status": args.status, "artifact": artifact},
    )
    atomic_write(manifest_path, data)
    print(json.dumps({"scene_id": args.scene_id, "status": args.status}, ensure_ascii=False))
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    data = load_manifest(manifest_path)
    if args.status == "waived" and (not args.reviewer or not args.note):
        raise SystemExit("A waived gate requires --reviewer and --note")
    gate = data["acceptance_gates"][args.name]
    gate.update(
        {
            "status": args.status,
            "evidence": args.evidence,
            "reviewer": args.reviewer,
            "note": args.note,
            "updated_at": utc_now(),
        }
    )
    append_history(data, "gate", {"name": args.name, "status": args.status})
    atomic_write(manifest_path, data)
    print(json.dumps({"gate": args.name, "status": args.status}, ensure_ascii=False))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    data = load_manifest(manifest_path)
    root = project_root(data)
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        errors.append(f"project root missing: {root}")
    artifacts = {item["path"]: item for item in data.get("artifacts", [])}
    selected_hashes: dict[str, str] = {}
    for scene in data.get("scenes", []):
        state = scene.get("status")
        if state not in SCENE_STATES:
            errors.append(f"{scene.get('scene_id')}: invalid state {state!r}")
        selected = scene.get("selected_artifact")
        if state in {"generated", "technically_verified", "needs_revision", "accepted"} and not selected:
            errors.append(f"{scene['scene_id']}: state {state} requires selected_artifact")
        if selected:
            path = ensure_within(root, root / selected)
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"{scene['scene_id']}: selected artifact missing or empty: {selected}")
            record = artifacts.get(selected)
            if record and record.get("sha256"):
                digest = record["sha256"]
                if digest in selected_hashes:
                    errors.append(
                        f"byte-identical selected scene files: {selected_hashes[digest]} and {scene['scene_id']}"
                    )
                selected_hashes[digest] = scene["scene_id"]
                media = record.get("media") or {}
                if media.get("probe_error"):
                    errors.append(f"{scene['scene_id']}: ffprobe failed: {media['probe_error']}")
            elif selected not in artifacts:
                warnings.append(f"{scene['scene_id']}: selected artifact not in last scan")
    roles = [item.get("role") for item in data.get("artifacts", [])]
    if args.release_ready:
        if "final_video" not in roles:
            errors.append("release requires a final_video artifact")
        if "cover" not in roles:
            errors.append("release requires a cover artifact")
        for scene in data.get("scenes", []):
            if scene.get("status") != "accepted":
                errors.append(f"release requires accepted scene: {scene.get('scene_id')}")
        for name in GATE_NAMES:
            status = data.get("acceptance_gates", {}).get(name, {}).get("status")
            if status != "pass":
                errors.append(f"release gate not passed: {name} ({status or 'missing'})")
    report = {
        "ok": not errors,
        "release_ready_checked": bool(args.release_ready),
        "errors": errors,
        "warnings": warnings,
        "scene_count": len(data.get("scenes", [])),
        "artifact_count": len(data.get("artifacts", [])),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a new manifest")
    init.add_argument("--root", required=True)
    init.add_argument("--project-id", required=True)
    init.add_argument("--brand-profile-id", required=True)
    init.add_argument("--scene", action="append", required=True, type=parse_scene)
    init.add_argument("--brief-source")
    init.add_argument("--channel")
    init.add_argument("--aspect-ratio", default="16:9")
    init.add_argument("--target-duration", type=float)
    init.add_argument("--filename", default="video-production-manifest.json")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    scan = subparsers.add_parser("scan", help="discover and fingerprint artifacts")
    scan.add_argument("--manifest", required=True)
    scan.add_argument("--glob", action="append", help="additional project-relative glob")
    scan.set_defaults(func=cmd_scan)

    scene = subparsers.add_parser("set-scene", help="update one scene and optionally log an attempt")
    scene.add_argument("--manifest", required=True)
    scene.add_argument("--scene-id", required=True)
    scene.add_argument("--status", required=True, choices=sorted(SCENE_STATES))
    scene.add_argument("--artifact")
    scene.add_argument("--attempt-status", choices=("submitted", "succeeded", "failed", "rejected", "blocked"))
    scene.add_argument("--provider")
    scene.add_argument("--note")
    scene.set_defaults(func=cmd_set_scene)

    gate = subparsers.add_parser("gate", help="record a final acceptance gate")
    gate.add_argument("--manifest", required=True)
    gate.add_argument("--name", required=True, choices=GATE_NAMES)
    gate.add_argument("--status", required=True, choices=sorted(GATE_STATES))
    gate.add_argument("--evidence")
    gate.add_argument("--reviewer")
    gate.add_argument("--note")
    gate.set_defaults(func=cmd_gate)

    validate = subparsers.add_parser("validate", help="validate manifest and release invariants")
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--release-ready", action="store_true")
    validate.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
