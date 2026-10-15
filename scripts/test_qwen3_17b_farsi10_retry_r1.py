#!/usr/bin/env python3
"""Three no-network corrected-retry preparation tests; no GitHub inference authorization."""
import importlib
import os
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

if __name__=="__main__":
    unittest.main()
