#!/usr/bin/env python3
"""Three no-network corrected-retry preparation tests; no GitHub inference authorization."""
import importlib
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

s=importlib.import_module("qwen3_17b_stage_verified_inference_RETRY_R1")
OLD=".github/workflows/qwen3-17b-farsi-inference-one-shot.yml@refs/heads/main"
NEW=".github/workflows/qwen3-17b-farsi-inference-retry-r1.yml@refs/heads/main"
REPO="nasrinabdollahkhani-bit/persian-llm-free-test"
ENV={
    "GITHUB_ACTIONS":"true", "GITHUB_REPOSITORY":REPO,
    "GITHUB_REF":"refs/heads/main", "GITHUB_ACTOR":"nasrinabdollahkhani-bit",
    "GITHUB_EVENT_NAME":"workflow_dispatch", "GITHUB_RUN_NUMBER":"1",
    "GITHUB_RUN_ATTEMPT":"1", "RUNNER_OS":"Linux", "GITHUB_JOB":"persian10",
    "GITHUB_WORKFLOW_REF":REPO+"/"+NEW,
}

class CorrectedRetryPreflight(unittest.TestCase):
    def test_only_new_manual_workflow_first_run_accepted(self):
        with mock.patch.dict(os.environ, ENV, clear=True):
            s.verify_context()

    def test_original_workflow_rejected(self):
        with mock.patch.dict(os.environ, dict(ENV,GITHUB_WORKFLOW_REF=REPO+"/"+OLD), clear=True):
            with self.assertRaisesRegex(RuntimeError,"ONE_SHOT_CONTEXT_DENIED"):
                s.verify_context()

    def test_second_run_or_attempt_rejected(self):
        for patch in ({"GITHUB_RUN_NUMBER":"2"},{"GITHUB_RUN_ATTEMPT":"2"}):
            with self.subTest(patch=patch):
                with mock.patch.dict(os.environ,dict(ENV,**patch),clear=True):
                    with self.assertRaisesRegex(RuntimeError,"ONE_SHOT_CONTEXT_DENIED"):
                        s.verify_context()


    def test_retry_stager_manifest_invalid_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=pathlib.Path(tmp)
            root=base/"empty-model"
            root.mkdir()
            malformed=base/"malformed.json"
            malformed.write_text("{}", encoding="utf-8")
            lock=pathlib.Path(__file__).resolve().parents[1]/"metadata/qwen3_17b_prior_acquisition_11_sha_lock.json"
            with mock.patch.object(s, "verify_context", return_value=None):
                with mock.patch.object(s, "download_one", side_effect=AssertionError("NETWORK")) as fn:
                    with self.assertRaises((ValueError, KeyError)):
                        s.stage(root, malformed, lock)
                    fn.assert_not_called()

    def test_retry_stager_dirty_directory_rejected_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=pathlib.Path(tmp)
            root=base/"model"
            root.mkdir()
            (root/"stray.file").write_text("fake", encoding="utf-8")
            manifest=pathlib.Path(__file__).resolve().parents[1]/"metadata/qwen3_17b_pinned_manifest.json"
            lock=pathlib.Path(__file__).resolve().parents[1]/"metadata/qwen3_17b_prior_acquisition_11_sha_lock.json"
            with mock.patch.object(s, "verify_context", return_value=None):
                with mock.patch.object(s, "download_one", side_effect=AssertionError("NETWORK")) as fn:
                    with self.assertRaisesRegex(RuntimeError, "UNSAFE_MODEL_DIR"):
                        s.stage(root, manifest, lock)
                    fn.assert_not_called()

    def test_retry_stager_eleven_hashes_mock_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            metadata=pathlib.Path(__file__).resolve().parents[1]/"metadata"
            lock=metadata/"qwen3_17b_prior_acquisition_11_sha_lock.json"
            manifest=metadata/"qwen3_17b_pinned_manifest.json"
            hashes=json.loads(lock.read_text(encoding="utf-8"))["sha256"]
            seen=[]
            def fake_download(model_root,entry):
                self.assertEqual(model_root, root.resolve())
                seen.append(entry["name"])
                return {"public_filename":entry["name"],"sha256_received":hashes[entry["name"]]}
            with mock.patch.object(s,"verify_context",return_value=None):
                with mock.patch.object(s,"download_one",side_effect=fake_download):
                    result=s.stage(root,manifest,lock)
            self.assertEqual(result["status"],"STAGED_11_OF_11_PREVIOUS_SHA_MATCH")
            self.assertEqual(len(seen),11)
            self.assertEqual(set(seen),set(hashes))

    def test_retry_stager_rejects_mismatched_download_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            metadata=pathlib.Path(__file__).resolve().parents[1]/"metadata"
            with mock.patch.object(s,"verify_context",return_value=None):
                with mock.patch.object(s,"download_one",return_value={"sha256_received":"0"*64}):
                    with self.assertRaisesRegex(RuntimeError,"PREVIOUS_RECEIPT_SHA_MISMATCH"):
                        s.stage(root,metadata/"qwen3_17b_pinned_manifest.json",
                                metadata/"qwen3_17b_prior_acquisition_11_sha_lock.json")


if __name__=="__main__":
    unittest.main()
