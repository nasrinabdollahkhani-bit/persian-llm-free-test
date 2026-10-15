#!/usr/bin/env python3
"""NO-network, NO-download, NO-inference tests for the hard-locked candidate."""
import importlib
import json
import os
import pathlib
import unittest
from unittest import mock

d = importlib.import_module("qwen3_17b_acquisition_PREPARED_LOCKED")
g = importlib.import_module("qwen3_17b_metadata_gate")
MANIFEST = (
    pathlib.Path(__file__).resolve().parents[1] /
    "metadata" / "qwen3_17b_pinned_manifest.json"
)


class LockedAcquisitionContracts(unittest.TestCase):
    def test_hard_lock_is_false(self):
        self.assertIs(d.ACQUISITION_ENABLED, False)

    def test_hard_lock_rejects_before_chat_approval(self):
        with self.assertRaisesRegex(RuntimeError, "STOP_NO_EXPLICIT_OWNER_CHAT_CONSENT"):
            d.assert_acquisition_authorized()

    def test_environment_cannot_unlock_hard_lock(self):
        with mock.patch.dict(os.environ, {"MORTEZA5_PRIVATE_OWNER_GATE_ATTESTED": "1"}):
            with self.assertRaisesRegex(RuntimeError, "STOP_NO_EXPLICIT_OWNER_CHAT_CONSENT"):
                d.assert_acquisition_authorized()

    def test_full_run_is_blocked_before_any_download(self):
        with mock.patch.object(d, "verify_context", return_value=None):
            with mock.patch.object(d.subprocess, "run", side_effect=AssertionError("NETWORK CALLED")) as call:
                report, code = d.run(MANIFEST)
        self.assertEqual(code, 2)
        self.assertEqual(report["reason_code"], "STOP_NO_EXPLICIT_OWNER_CHAT_CONSENT")
        self.assertEqual(report["file_digests"], [])
        self.assertEqual(report["model_execution"], "NOT_EXECUTED")
        call.assert_not_called()

    def test_exact_immutable_repo_and_revision(self):
        self.assertEqual(d.MODEL, "Qwen/Qwen3-1.7B")
        self.assertEqual(d.REV, "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e")

    def test_allowlist_exactly_matches_manifest(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(tuple(x["name"] for x in m["required_files"]), d.FILES)
        self.assertEqual(len(d.FILES), 11)
        self.assertEqual(len(set(d.FILES)), 11)
        g.validate_manifest(m)

    def test_three_published_digest_constraints(self):
        self.assertEqual(len(d.SHA), 3)
        self.assertEqual(len([x for x in d.FILES if x.endswith(".safetensors")]), 2)
        self.assertTrue(all(len(v) == 64 for v in d.SHA.values()))

    def test_non_allowlisted_filename_rejected_without_network(self):
        with mock.patch.object(d.subprocess, "run", side_effect=AssertionError("NETWORK CALLED")) as call:
            with self.assertRaisesRegex(RuntimeError, "DISALLOWED_MODEL_FILENAME"):
                d.download_one(pathlib.Path("/tmp"), {"name": "../secret.txt"})
        call.assert_not_called()

    def test_metadata_contract_does_not_grant_download(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(m["authorization"]["model_acquisition"], "NOT_AUTHORIZED_BY_THIS_MANIFEST")
        self.assertEqual(m["authorization"]["model_inference"], "NOT_AUTHORIZED")

    def test_receipt_schema_not_weights(self):
        self.assertEqual(d.RECEIPT_FILE, "qwen3_17b_acquisition_sha_only_receipt.json")
        self.assertGreater(d.MIN_DISK_FREE_BYTES, 10 * 1024**3)


if __name__ == "__main__":
    unittest.main()
