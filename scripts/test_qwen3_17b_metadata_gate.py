#!/usr/bin/env python3
"""Model-free test suite. Does not download anything or run a model."""
import copy
import importlib
import json
import pathlib
import unittest

m = importlib.import_module("qwen3_17b_metadata_gate")
MANIFEST = pathlib.Path(__file__).resolve().parents[1] / "metadata" / "qwen3_17b_pinned_manifest.json"


class TestQwen17MetadataGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def manifest(self):
        return copy.deepcopy(self.original)

    def test_exact_revision_and_repo(self):
        self.assertEqual(m.REV, "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e")
        self.assertEqual(m.MODEL, "Qwen/Qwen3-1.7B")

    def test_real_manifest_passes_static_provenance_gate(self):
        r = m.validate_manifest(self.manifest())
        self.assertEqual(r["allowlisted_files"], 11)
        self.assertEqual(r["independently_published_sha256_count"], 3)

    def test_rejects_mutable_revision(self):
        x = self.manifest()
        x["fixed_revision"] = "main"
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_rejects_missing_or_extra_files(self):
        x = self.manifest()
        x["required_files"].pop()
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_rejects_weight_sha_tampering(self):
        x = self.manifest()
        x["required_files"][5]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_rejects_weight_size_tampering(self):
        x = self.manifest()
        x["required_files"][5]["bytes"] -= 1
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_no_unpublished_hash_claims(self):
        x = self.manifest()
        x["required_files"][0]["sha256"] = "a" * 64
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_acquisition_authorization_cannot_be_smuggled_in(self):
        x = self.manifest()
        x["authorization"]["model_acquisition"] = "AUTHORIZED"
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_inference_authorization_cannot_be_smuggled_in(self):
        x = self.manifest()
        x["authorization"]["model_inference"] = "AUTHORIZED"
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_no_paid_runner_or_org_data(self):
        x = self.manifest()
        x["authorization"]["paid_runners"] = "ALLOWED"
        with self.assertRaises(ValueError):
            m.validate_manifest(x)

    def test_preflight_never_claims_model_fit(self):
        s = m.capacity_snapshot()
        self.assertIs(s["model_runtime_memory_fit_proven"], False)


if __name__ == "__main__":
    unittest.main()
