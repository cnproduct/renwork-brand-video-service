#!/usr/bin/env python3
"""Append-only registry helper for reviewed RenWork video-production knowledge."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
RECORD_TYPES = ("asset", "knowledge", "glossary", "faq", "success_pattern")
EVIDENCE_STATES = {"VERIFIED", "INTERNAL", "PILOT", "ASSUMPTION", "DISPUTED", "RETIRED"}
RISK_LEVELS = {"low", "medium", "high"}
INPUT_KINDS = {"text", "audio", "video", "image", "manifest"}
AUTHORITATIVE_SOURCE_TYPES = {"primary_authority", "official_product"}

TYPE_REQUIRED = {
    "asset": {"id", "title", "sources", "input_kind", "source_uri", "rights_status", "privacy_classification"},
    "knowledge": {"id", "title", "sources", "claim", "domain", "evidence_status", "risk_level", "applicability"},
    "glossary": {"id", "title", "sources", "canonical", "variants", "domain", "language", "validation_note"},
    "faq": {
        "id", "title", "sources", "symptom", "impact", "pipeline_stage", "root_cause_status",
        "root_cause", "resolution", "validation", "rollback", "prevention", "scope_limits",
    },
    "success_pattern": {
        "id", "title", "sources", "artifact_uri", "artifact_sha256", "manifest_uri",
        "user_approved", "qa_evidence", "pattern", "applicability", "scope_limits",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_root(args: argparse.Namespace) -> Path:
    if not args.kb_root:
        raise ValueError("Provide --kb-root ROOT")
    return args.kb_root.expanduser().resolve()


def registry_path(root: Path, area: str, record_type: str) -> Path:
    return root / area / f"{record_type}.jsonl"


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(source: str) -> dict[str, Any]:
    if source.strip().startswith("{"):
        value = json.loads(source)
    else:
        with Path(source).expanduser().open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("Record JSON must contain one object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            records.append(value)
    return records


def load_metadata(root: Path) -> dict[str, Any]:
    metadata_path = root / "kb.json"
    if not metadata_path.is_file():
        raise ValueError(f"Not an initialized RenWork video knowledge base: {root}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for field in ("tenant_id", "brand_profile_id"):
        if not metadata.get(field):
            raise ValueError(f"kb.json missing {field}")
    return metadata


def apply_scope(record: dict[str, Any], metadata: dict[str, Any]) -> None:
    for field in ("tenant_id", "brand_profile_id"):
        expected = metadata[field]
        supplied = record.get(field)
        if supplied is not None and supplied != expected:
            raise ValueError(f"{field} conflicts with initialized scope")
        record[field] = expected


def validate_record(record: dict[str, Any], record_type: str, approved: bool = False) -> list[str]:
    errors: list[str] = []
    missing = sorted((TYPE_REQUIRED[record_type] | {"tenant_id", "brand_profile_id"}) - record.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    sources = record.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
    elif any(not isinstance(source, dict) or not source.get("uri") for source in sources):
        errors.append("every source must be an object with a non-empty uri")

    if record_type == "asset" and record.get("input_kind") not in INPUT_KINDS:
        errors.append(f"input_kind must be one of: {', '.join(sorted(INPUT_KINDS))}")

    if record_type == "knowledge":
        if record.get("evidence_status") not in EVIDENCE_STATES:
            errors.append(f"evidence_status must be one of: {', '.join(sorted(EVIDENCE_STATES))}")
        if record.get("risk_level") not in RISK_LEVELS:
            errors.append(f"risk_level must be one of: {', '.join(sorted(RISK_LEVELS))}")
        if record.get("evidence_status") == "VERIFIED":
            source_types = {item.get("source_type") for item in sources or [] if isinstance(item, dict)}
            if not source_types.intersection(AUTHORITATIVE_SOURCE_TYPES):
                errors.append("VERIFIED knowledge requires a primary_authority or official_product source")
        if approved and record.get("evidence_status") in {"ASSUMPTION", "DISPUTED", "RETIRED"}:
            errors.append("ASSUMPTION, DISPUTED, or RETIRED knowledge cannot enter the approved registry")
        if approved and record.get("risk_level") == "high":
            if not record.get("review_due"):
                errors.append("approved high-risk knowledge requires review_due")
            if not record.get("prohibited_overstatement"):
                errors.append("approved high-risk knowledge requires prohibited_overstatement")

    if record_type == "glossary" and not isinstance(record.get("variants"), list):
        errors.append("variants must be a list")

    if record_type == "faq":
        if record.get("root_cause_status") not in {"confirmed", "hypothesis"}:
            errors.append("root_cause_status must be confirmed or hypothesis")
        if not isinstance(record.get("validation"), list):
            errors.append("validation must be a list")
        if approved and record.get("root_cause_status") == "hypothesis":
            errors.append("a hypothesis FAQ cannot be approved as a deterministic solution")

    if record_type == "success_pattern":
        if not isinstance(record.get("qa_evidence"), list):
            errors.append("qa_evidence must be a list")
        artifact_hash = record.get("artifact_sha256")
        if not isinstance(artifact_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", artifact_hash):
            errors.append("artifact_sha256 must be a lowercase 64-character SHA-256")
        if approved and record.get("user_approved") is not True:
            errors.append("approved success_pattern requires user_approved=true")
        if approved and not record.get("qa_evidence"):
            errors.append("approved success_pattern requires non-empty qa_evidence")

    if approved:
        approval = record.get("approval")
        if not isinstance(approval, dict):
            errors.append("approved record requires approval object")
        else:
            for key in ("reviewer", "reviewed_at", "note"):
                if not approval.get(key):
                    errors.append(f"approval.{key} is required")
    return errors


def cmd_init(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    if root.exists() and any(root.iterdir()):
        raise ValueError(f"Refusing to initialize non-empty directory: {root}")
    root.mkdir(parents=True, exist_ok=True)
    for area in ("staging", "approved"):
        (root / area).mkdir()
        for record_type in RECORD_TYPES:
            registry_path(root, area, record_type).touch()
    (root / "reviews").mkdir()
    (root / "retired").mkdir()
    metadata = {
        "name": "RenWork video production knowledge base",
        "schema_version": SCHEMA_VERSION,
        "tenant_id": args.tenant_id,
        "brand_profile_id": args.brand_profile_id,
        "created_at": utc_now(),
        "policy": "staged records require explicit review before approval",
    }
    (root / "kb.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(root)
    return 0


def cmd_stage(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    metadata = load_metadata(root)
    record = load_json(args.record)
    apply_scope(record, metadata)
    record.setdefault("id", f"{args.record_type}-{uuid.uuid4().hex[:12]}")
    record.setdefault("schema_version", SCHEMA_VERSION)
    record["record_type"] = args.record_type
    record["state"] = "STAGED"
    record.setdefault("created_at", utc_now())
    errors = validate_record(record, args.record_type)
    if errors:
        raise ValueError("; ".join(errors))
    existing = load_jsonl(registry_path(root, "staging", args.record_type))
    if any(item.get("id") == record["id"] for item in existing):
        raise ValueError(f"Duplicate staged id: {record['id']}")
    append_jsonl(registry_path(root, "staging", args.record_type), record)
    print(record["id"])
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    metadata = load_metadata(root)
    staged = load_jsonl(registry_path(root, "staging", args.record_type))
    matches = [record for record in staged if record.get("id") == args.record_id]
    if not matches:
        raise ValueError(f"No staged {args.record_type} record with id {args.record_id}")
    approved_existing = load_jsonl(registry_path(root, "approved", args.record_type))
    if any(record.get("id") == args.record_id for record in approved_existing):
        raise ValueError(f"Record is already approved: {args.record_id}")
    record = dict(matches[-1])
    apply_scope(record, metadata)
    record["state"] = "APPROVED"
    record["approval"] = {"reviewer": args.reviewer, "reviewed_at": utc_now(), "note": args.note}
    errors = validate_record(record, args.record_type, approved=True)
    if errors:
        raise ValueError("; ".join(errors))
    append_jsonl(registry_path(root, "approved", args.record_type), record)
    append_jsonl(root / "reviews" / "promotion_log.jsonl", {
        "event_id": f"review-{uuid.uuid4().hex[:12]}",
        "record_id": args.record_id,
        "record_type": args.record_type,
        "tenant_id": metadata["tenant_id"],
        "brand_profile_id": metadata["brand_profile_id"],
        "action": "APPROVED",
        "reviewer": args.reviewer,
        "reviewed_at": record["approval"]["reviewed_at"],
        "note": args.note,
    })
    print(args.record_id)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    metadata = load_metadata(root)
    errors: list[str] = []
    for area in ("staging", "approved"):
        for record_type in RECORD_TYPES:
            path = registry_path(root, area, record_type)
            try:
                records = load_jsonl(path)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            seen: set[str] = set()
            for index, record in enumerate(records, 1):
                record_id = str(record.get("id", ""))
                if record_id in seen:
                    errors.append(f"{path}:{index}: duplicate id {record_id}")
                seen.add(record_id)
                if record.get("record_type") != record_type:
                    errors.append(f"{path}:{index}: record_type mismatch")
                expected_state = "APPROVED" if area == "approved" else "STAGED"
                if record.get("state") != expected_state:
                    errors.append(f"{path}:{index}: expected state {expected_state}")
                for field in ("tenant_id", "brand_profile_id"):
                    if record.get(field) != metadata[field]:
                        errors.append(f"{path}:{index}: {field} scope mismatch")
                for problem in validate_record(record, record_type, approved=(area == "approved")):
                    errors.append(f"{path}:{index}: {problem}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("OK")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize an empty knowledge-base root")
    init_parser.add_argument("--kb-root", type=Path, required=True)
    init_parser.add_argument("--tenant-id", required=True)
    init_parser.add_argument("--brand-profile-id", required=True)
    init_parser.set_defaults(func=cmd_init)

    stage_parser = subparsers.add_parser("stage", help="validate and append a staged record")
    stage_parser.add_argument("--kb-root", type=Path, required=True)
    stage_parser.add_argument("--type", dest="record_type", choices=RECORD_TYPES, required=True)
    stage_parser.add_argument("--record", required=True)
    stage_parser.set_defaults(func=cmd_stage)

    approve_parser = subparsers.add_parser("approve", help="promote an explicitly reviewed staged record")
    approve_parser.add_argument("--kb-root", type=Path, required=True)
    approve_parser.add_argument("--type", dest="record_type", choices=RECORD_TYPES, required=True)
    approve_parser.add_argument("--id", dest="record_id", required=True)
    approve_parser.add_argument("--reviewer", required=True)
    approve_parser.add_argument("--note", required=True)
    approve_parser.set_defaults(func=cmd_approve)

    validate_parser = subparsers.add_parser("validate", help="validate every staged and approved registry")
    validate_parser.add_argument("--kb-root", type=Path, required=True)
    validate_parser.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
