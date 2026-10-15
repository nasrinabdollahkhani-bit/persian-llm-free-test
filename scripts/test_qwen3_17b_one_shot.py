#!/usr/bin/env python3
"""Public synthetic-only one-shot gate tests. NO network/download/inference."""
import copy
import importlib
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

a = importlib.import_module("qwen3_17b_acquisition_ONE_SHOT")
m = importlib.import_module("qwen3_17b_metadata_gate")
MANIFEST = pathlib.Path(__file__).resolve().parents[1] / "metadata" / "qwen3_17b_pinned_manifest.json"

GOOD_ENV = {
    "GITHUB_WORKFLOW_REF": a.WORKFLOW_REF,
    "GITHUB_RUN_NUMBER": "1",
    "GITHUB_RUN_ATTEMPT": "1",
    "GITHUB_JOB": "acquire_only",
}


class OneShotAcquisitionContracts(unittest.TestCase):
    def test_exact_model_revision(self):
        self.assertEqual(a.MODEL, "Qwen/Qwen3-1.7B")
        self.assertEqual(a.REV, "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e")

    def test_only_one_specific_workflow_allowed(self):
        self.assertEqual(a.WORKFLOW_REF, "nasrinabdollahkhani-bit/persian-llm-free-test/.github/workflows/qwen3-17b-one-shot-acquisition.yml@refs/heads/main")

    def test_first_run_first_attempt_passes_controlled_context(self):
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.dict(os.environ, GOOD_ENV):
                a.check_one_shot()

    def test_rejects_run_two(self):
        bad = dict(GOOD_ENV, GITHUB_RUN_NUMBER="2")
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.dict(os.environ, bad):
                with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED_GITHUB_RUN_NUMBER"):
                    a.check_one_shot()

    def test_rejects_rerun_attempt(self):
        bad = dict(GOOD_ENV, GITHUB_RUN_ATTEMPT="2")
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.dict(os.environ, bad):
                with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED_GITHUB_RUN_ATTEMPT"):
                    a.check_one_shot()

    def test_rejects_unapproved_workflow(self):
        bad = dict(GOOD_ENV, GITHUB_WORKFLOW_REF="elsewhere@refs/heads/main")
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.dict(os.environ, bad):
                with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED_GITHUB_WORKFLOW_REF"):
                    a.check_one_shot()

    def test_rejects_other_job(self):
        bad = dict(GOOD_ENV, GITHUB_JOB="other")
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.dict(os.environ, bad):
                with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED_GITHUB_JOB"):
                    a.check_one_shot()

    def test_rejected_context_makes_no_download_calls(self):
        with mock.patch.object(a.locked, "verify_context", return_value=None):
            with mock.patch.object(a.locked, "download_one", side_effect=AssertionError("NETWORK CALLED")) as fn:
                with mock.patch.dict(os.environ, dict(GOOD_ENV, GITHUB_RUN_NUMBER="2")):
                    report, rc = a.acquire(MANIFEST)
        self.assertEqual(rc, 2)
        self.assertEqual(report["file_digests"], [])
        self.assertEqual(report["status"], "BLOCKED")
        fn.assert_not_called()

    def test_manifest_prechecked_before_any_download(self):
        malformed = json.loads(MANIFEST.read_text(encoding="utf-8"))
        malformed["fixed_revision"] = "main"
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "manifest.json"
            path.write_text(json.dumps(malformed), encoding="utf-8")
            with mock.patch.object(a, "check_one_shot", return_value=None):
                with mock.patch.object(a.locked, "download_one", side_effect=AssertionError("NETWORK CALLED")) as fn:
                    report, rc = a.acquire(path)
        self.assertEqual(rc, 2)
        fn.assert_not_called()

    def test_allowlist_mock_without_real_downloading(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        visited = []
        def mock_one(root, entry):
            self.assertTrue(str(root).startswith(tempfile.gettempdir()))
            visited.append(entry["name"])
            return {
                "public_filename": entry["name"],
                "bytes_received": 20,
                "sha256_received": "0" * 64,
                "published_sha256": entry.get("sha256"),
                "verification": "UNIT_TEST_MOCK_NOT_REAL_EVIDENCE",
            }
        with mock.patch.object(a, "check_one_shot", return_value=None):
            with mock.patch.object(a.locked, "download_one", side_effect=mock_one) as fn:
                report, rc = a.acquire(MANIFEST)
        self.assertEqual(rc, 0)
        self.assertEqual(len(report["file_digests"]), 11)
        self.assertEqual(visited, [x["name"] for x in manifest["required_files"]])
        self.assertEqual(report["model_inference"], "NOT_EXECUTED")
        self.assertEqual(report["temporary_model_bytes"], "DELETED_ON_NORMAL_EXIT")
        self.assertEqual(fn.call_count, 11)

    def test_upstream_sha_mismatch_rejected_with_fake_bytes(self):
        class Ret:
            returncode = 0
        entry = {"name": "tokenizer.json", "bytes": None}
        def no_net_cmd(cmd, **kwargs):
            pathlib.Path(cmd[cmd.index("--output") + 1]).write_bytes(b"synthetic dummy bytes")
            return Ret()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(a.locked.subprocess, "run", side_effect=no_net_cmd):
                with self.assertRaisesRegex(RuntimeError, "PUBLISHED_SHA256_MISMATCH"):
                    a.locked.download_one(pathlib.Path(tmp), entry)

    def test_file_extension_does_not_bypass_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(a.locked.subprocess, "run", side_effect=AssertionError("NETWORK CALLED")) as fn:
                with self.assertRaisesRegex(RuntimeError, "DISALLOWED_MODEL_FILENAME"):
                    a.locked.download_one(pathlib.Path(tmp), {"name": "my-own.safetensors"})
            fn.assert_not_called()

    def test_inference_never_enabled_in_run_report(self):
        self.assertNotIn("transformers", a.__dict__)
        self.assertNotIn("torch", a.__dict__)
        self.assertIn("NO_INFERENCE", a.APPROVAL_SCOPE)

    def test_manifest_size_and_digests_static_contract(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        r = m.validate_manifest(manifest)
        self.assertEqual(r["published_shard_file_bytes"], 4063515592)
        self.assertEqual(r["independently_published_sha256_count"], 3)


if __name__ == "__main__":
    unittest.main()
