#!/usr/bin/env python3
"""16 no-network, no-weight and no-torch tests for Qwen3-1.7B FA10 workflow."""
import copy
import importlib
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

s = importlib.import_module("qwen3_17b_stage_verified_inference")
i = importlib.import_module("qwen3_17b_farsi10_inference")
q = importlib.import_module("qwen_farsi_quality_v2")
b = importlib.import_module("local_qwen_fa_smoke")
ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "metadata" / "qwen3_17b_pinned_manifest.json"
LOCK = ROOT / "metadata" / "qwen3_17b_prior_acquisition_11_sha_lock.json"


class Qwen17InferenceContracts(unittest.TestCase):
    def test_01_model_and_commit_are_immutable(self):
        self.assertEqual(i.MODEL, "Qwen/Qwen3-1.7B")
        self.assertEqual(i.REV, "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e")

    def test_02_prompt_count_is_exact_ten(self):
        self.assertEqual(len(i.PROMPTS), 10)
        self.assertEqual(len(set(i.PROMPTS)), 10)

    def test_03_identical_all_ten_v2_prompts(self):
        self.assertEqual(i.PROMPTS, q.PROMPTS)
        self.assertEqual(i.PROMPTS, b.PROMPTS)

    def test_04_identical_fewshot_system_seed(self):
        self.assertEqual(i.SYSTEM, q.SYSTEM)
        self.assertEqual(i.EXAMPLE, q.EXAMPLE)
        self.assertEqual(i.SEED, q.SEED)

    def test_05_identical_sampling_and_token_limit(self):
        self.assertEqual(i.GENERATION, q.GENERATION)
        self.assertFalse(i.GENERATION.get("enable_thinking", False))
        self.assertEqual(i.GENERATION["max_new_tokens"], 160)

    def test_06_thinking_disabled_profile_and_human_review(self):
        self.assertIn("NONTHINKING", i.PROFILE)
        self.assertEqual(i.EXPECTED_BASELINE, "38711873242")
        self.assertEqual(i.observable_only("سلام")["short_response_flag"], True)

    def test_07_exact_allowlist_and_published_hash_lock(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        self.assertEqual(len(m["required_files"]), 11)
        self.assertEqual(set(lock["sha256"]), set(s.FILES))
        self.assertEqual(s.REV, lock["fixed_revision"])
        self.assertEqual(lock["source_run_id"], "38734778931")

    def test_08_reject_tampered_prior_hash_lock(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        lock["sha256"]["tokenizer.json"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "PUBLISHED_SHA_CONFLICT"):
            s.validate_hash_lock(m, lock)

    def test_09_reject_mutable_revision(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        lock["fixed_revision"] = "main"
        with self.assertRaisesRegex(RuntimeError, "PRIOR_RECEIPT_IDENTITY_MISMATCH"):
            s.validate_hash_lock(m, lock)

    def test_10_reject_extra_file(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        lock["sha256"]["unknown.bin"] = "a" * 64
        with self.assertRaisesRegex(RuntimeError, "ALLOWLIST_MISMATCH"):
            s.validate_hash_lock(m, lock)

    def test_11_owner_one_shot_rejects_second_run(self):
        with mock.patch.dict(os.environ, {"GITHUB_RUN_NUMBER": "2"}):
            with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED"):
                s.verify_context()

    def test_12_owner_one_shot_rejects_second_attempt(self):
        env = {
            "GITHUB_ACTIONS": "true", "GITHUB_REPOSITORY": "nasrinabdollahkhani-bit/persian-llm-free-test",
            "GITHUB_REF": "refs/heads/main", "GITHUB_ACTOR": "nasrinabdollahkhani-bit",
            "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_RUN_NUMBER": "1",
            "GITHUB_RUN_ATTEMPT": "2", "RUNNER_OS": "Linux", "GITHUB_JOB": "persian10",
            "GITHUB_WORKFLOW_REF": "nasrinabdollahkhani-bit/persian-llm-free-test/.github/workflows/qwen3-17b-farsi-inference-one-shot.yml@refs/heads/main",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ONE_SHOT_CONTEXT_DENIED"):
                s.verify_context()

    def test_13_manifest_checked_before_any_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(s, "verify_context", return_value=None):
                with mock.patch.object(s, "download_one", side_effect=AssertionError("NETWORK")) as f:
                    base=pathlib.Path(tmp)
                    root=base/"empty_model"
                    root.mkdir()
                    wrong=base/"bad.json"
                    wrong.write_text("{}",encoding="utf-8")
                    with self.assertRaises((ValueError, KeyError)):
                        s.stage(root,wrong,LOCK)
                f.assert_not_called()

    def test_13b_nonempty_model_dir_fails_closed_before_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)/"model"
            root.mkdir()
            (root/"stray.txt").write_text("synthetic",encoding="utf-8")
            with mock.patch.object(s, "verify_context", return_value=None):
                with mock.patch.object(s, "download_one",
                                       side_effect=AssertionError("NETWORK")) as f:
                    with self.assertRaisesRegex(RuntimeError, "UNSAFE_MODEL_DIR"):
                        s.stage(root,MANIFEST,LOCK)
                f.assert_not_called()

    def test_14_all_eleven_mocked_downloads_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            lock=json.loads(LOCK.read_text(encoding="utf-8"))
            calls=[]
            def fake(root,entry):
                calls.append(entry["name"])
                return {"public_filename":entry["name"],"sha256_received":lock["sha256"][entry["name"]]}
            with mock.patch.object(s,"verify_context",return_value=None):
                with mock.patch.object(s,"download_one",side_effect=fake):
                    report=s.stage(root,MANIFEST,LOCK)
            self.assertEqual(len(calls),11)
            self.assertEqual(len(report["file_digests"]),11)
            self.assertEqual(report["status"],"STAGED_11_OF_11_PREVIOUS_SHA_MATCH")

    def test_15_reject_prior_sha_mismatch_after_mocked_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(s,"verify_context",return_value=None):
                with mock.patch.object(s,"download_one",return_value={"sha256_received":"0"*64}):
                    with self.assertRaisesRegex(RuntimeError,"PREVIOUS_RECEIPT_SHA_MISMATCH"):
                        s.stage(pathlib.Path(tmp),MANIFEST,LOCK)

    def test_16_inference_does_not_use_web_or_quality_auto_acceptance(self):
        self.assertNotIn("torch", i.__dict__)
        self.assertNotIn("transformers", i.__dict__)
        self.assertIn("NOT_AUTOMATICALLY_EVALUATED_HUMAN_REVIEW_REQUIRED",
                      ROOT.joinpath("scripts/qwen3_17b_farsi10_inference.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
