#!/usr/bin/env python3
"""Forward tests for the reviewed RenWork video knowledge registry."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "skills" / "renwork-video-production-knowledge-base" / "scripts" / "renwork_video_kb.py"


class VideoKnowledgeBaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="renwork-video-kb-")
        self.root = Path(self.temp_dir.name) / "kb"
        self.run_cli("init", "--kb-root", str(self.root), "--tenant-id", "tenant-a", "--brand-profile-id", "brand-a")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_cli(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, check=False)
        self.assertEqual(expected, result.returncode, msg=result.stderr or result.stdout)
        return result

    def stage(self, record_type: str, record: dict, expected: int = 0) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            "stage", "--kb-root", str(self.root), "--type", record_type,
            "--record", json.dumps(record, ensure_ascii=False), expected=expected,
        )

    def approve(self, record_type: str, record_id: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            "approve", "--kb-root", str(self.root), "--type", record_type, "--id", record_id,
            "--reviewer", "Brand QA", "--note", "Reviewed against source and final artifact", expected=expected,
        )

    def test_scope_is_injected_and_cross_tenant_record_is_rejected(self) -> None:
        record = {
            "id": "asset-manifest", "title": "Production manifest",
            "sources": [{"uri": "/project/video-production-manifest.json", "source_type": "user_asset"}],
            "input_kind": "manifest", "source_uri": "/project/video-production-manifest.json",
            "rights_status": "user_provided", "privacy_classification": "internal",
        }
        self.stage("asset", record)
        stored = json.loads((self.root / "staging" / "asset.jsonl").read_text(encoding="utf-8"))
        self.assertEqual("tenant-a", stored["tenant_id"])
        bad = dict(record, id="asset-wrong-tenant", tenant_id="tenant-b")
        result = self.stage("asset", bad, expected=2)
        self.assertIn("tenant_id conflicts", result.stderr)

    def test_hypothesis_faq_cannot_be_approved(self) -> None:
        record = {
            "id": "faq-drift-hypothesis", "title": "Possible duration drift",
            "sources": [{"uri": "/project/final.mp4", "source_type": "observed_output"}],
            "symptom": "Subtitle drift", "impact": "Picture and voice do not match", "pipeline_stage": "assembly",
            "root_cause_status": "hypothesis", "root_cause": "A source duration may have changed",
            "resolution": "Compare frozen source durations", "validation": [], "rollback": "Use last accepted composite",
            "prevention": "Freeze source inventory", "scope_limits": "Other timing errors can look similar",
        }
        self.stage("faq", record)
        result = self.approve("faq", record["id"], expected=2)
        self.assertIn("hypothesis FAQ cannot be approved", result.stderr)

    def test_verified_claim_requires_authoritative_source(self) -> None:
        record = {
            "id": "knowledge-unsupported", "title": "Unsupported verified claim",
            "sources": [{"uri": "https://example.com/summary", "source_type": "secondary"}],
            "claim": "A product capability is available", "domain": "product", "evidence_status": "VERIFIED",
            "risk_level": "high", "applicability": "Example only",
        }
        result = self.stage("knowledge", record, expected=2)
        self.assertIn("primary_authority or official_product", result.stderr)

    def test_accepted_video_pattern_can_be_promoted_with_manifest_and_qa(self) -> None:
        record = {
            "id": "pattern-scene-hook", "title": "Accepted three-second hook",
            "sources": [{"uri": "/project/final.mp4", "source_type": "observed_output"}],
            "artifact_uri": "/project/final.mp4", "artifact_sha256": "a" * 64,
            "manifest_uri": "/project/video-production-manifest.json", "user_approved": True,
            "qa_evidence": ["Human full playback passed", "Picture-subtitle-audio sync gate passed"],
            "pattern": "Open with the visible customer task before product explanation",
            "applicability": "Short RenWork training scene videos", "scope_limits": "Not validated for long-form films",
        }
        self.stage("success_pattern", record)
        self.approve("success_pattern", record["id"])
        self.assertEqual("OK", self.run_cli("validate", "--kb-root", str(self.root)).stdout.strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
