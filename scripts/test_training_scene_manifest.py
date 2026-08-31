#!/usr/bin/env python3
"""Forward tests for the RenWork training-scene artifact manifest."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

try:
    import jsonschema
except ImportError:  # Optional in minimal runtime installs.
    jsonschema = None


REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "skills" / "renwork-training-scene-videos" / "scripts" / "artifact_manifest.py"
SCHEMA = REPO / "schemas" / "video-production-manifest.schema.json"
GATES = (
    "technical_playback",
    "scene_content_match",
    "picture_subtitle_audio_sync",
    "no_duplicate_footage",
    "brand_consistency",
    "cover_applied",
    "human_review",
)


def run_tool(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(TOOL), *args],
        text=True,
        capture_output=True,
        check=check,
    )


class TrainingSceneManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="renwork-training-scenes-")
        self.root = Path(self.tempdir.name).resolve()
        self.manifest = self.root / "video-production-manifest.json"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def init_manifest(self) -> None:
        run_tool(
            "init",
            "--root",
            str(self.root),
            "--project-id",
            "forward-test",
            "--brand-profile-id",
            "renwork",
            "--scene",
            "1:training_classroom:全员实操培训",
        )

    def test_skill_and_schema_are_discoverable(self) -> None:
        skill = REPO / "skills" / "renwork-training-scene-videos" / "SKILL.md"
        self.assertTrue(skill.is_file())
        self.assertNotIn("TODO", skill.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "RenWorkVideoProductionManifest")

    def test_init_is_resumable_and_refuses_overwrite(self) -> None:
        self.init_manifest()
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["scenes"][0]["status"], "planned")
        if jsonschema is not None:
            schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            jsonschema.validate(data, schema)
        second = run_tool(
            "init",
            "--root",
            str(self.root),
            "--project-id",
            "forward-test",
            "--brand-profile-id",
            "renwork",
            "--scene",
            "1:training_classroom:全员实操培训",
            check=False,
        )
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("Refusing to overwrite", second.stderr)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg is required")
    def test_release_requires_scenes_and_all_human_gates(self) -> None:
        self.init_manifest()
        scene = self.root / "scene1_training_classroom.mp4"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "color=c=black:s=320x180:d=0.25",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=stereo",
                "-shortest",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                str(scene),
            ],
            check=True,
            capture_output=True,
        )
        shutil.copy2(scene, self.root / "renwork_training_v01_final.mp4")
        (self.root / "renwork_training_cover.png").write_bytes(b"fixture-cover")
        (self.root / "renwork_training_wechat_copy.md").write_text("fixture copy\n", encoding="utf-8")

        run_tool("scan", "--manifest", str(self.manifest))
        generated = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(generated["scenes"][0]["status"], "generated")

        blocked = run_tool(
            "validate",
            "--manifest",
            str(self.manifest),
            "--release-ready",
            check=False,
        )
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("release requires accepted scene", blocked.stdout)
        self.assertIn("human_review", blocked.stdout)

        run_tool(
            "set-scene",
            "--manifest",
            str(self.manifest),
            "--scene-id",
            "scene1",
            "--status",
            "accepted",
            "--artifact",
            scene.name,
            "--attempt-status",
            "succeeded",
            "--provider",
            "fixture-provider",
        )
        for gate in GATES:
            run_tool(
                "gate",
                "--manifest",
                str(self.manifest),
                "--name",
                gate,
                "--status",
                "pass",
                "--reviewer",
                "fixture-reviewer",
                "--evidence",
                "isolated forward test",
            )

        release = run_tool(
            "validate",
            "--manifest",
            str(self.manifest),
            "--release-ready",
        )
        self.assertTrue(json.loads(release.stdout)["ok"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
