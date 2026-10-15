#!/usr/bin/env python3
"""ONE authorised public model acquisition, SHA check, and cleanup; NO inference.

Authorization: owner explicitly approved in chat on 2026-10-15 the acquisition
of the 11 public Qwen3-1.7B files at the exact pinned commit once on the
standard, free, public GitHub-hosted Ubuntu CPU runner. Inference is NOT
approved. This is not a production or Windows-security validation.
"""
import argparse
import json
import os
import pathlib
import tempfile
from datetime import datetime, timezone

import qwen3_17b_acquisition_PREPARED_LOCKED as locked
from qwen3_17b_metadata_gate import MODEL, REV, validate_manifest

APPROVAL_SCOPE = "CHAT_OWNER_APPROVED_2026-10-15_ONE_ACQUISITION_NO_INFERENCE"
WORKFLOW_REF = (
    "nasrinabdollahkhani-bit/persian-llm-free-test/"
    ".github/workflows/qwen3-17b-one-shot-acquisition.yml@refs/heads/main"
)
EXPECTED_RUN_NUMBER = "1"
EXPECTED_RUN_ATTEMPT = "1"


def check_one_shot():
    """Reject unauthorized actors, non-standard run context, retries, and repeat runs."""
    locked.verify_context()
    required = {
        "GITHUB_WORKFLOW_REF": WORKFLOW_REF,
        "GITHUB_RUN_NUMBER": EXPECTED_RUN_NUMBER,
        "GITHUB_RUN_ATTEMPT": EXPECTED_RUN_ATTEMPT,
        "GITHUB_JOB": "acquire_only",
    }
    for key, expected in required.items():
        if os.environ.get(key) != expected:
            raise RuntimeError("ONE_SHOT_CONTEXT_DENIED_" + key)


def acquire(manifest_path):
    receipt = {
        "schema": "morteza5.public.qwen3-1.7b.one-shot-acquisition.v1",
        "model": MODEL,
        "immutable_revision": REV,
        "owner_consent_scope": APPROVAL_SCOPE,
        "git_run_id": os.environ.get("GITHUB_RUN_ID"),
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "model_inference": "NOT_EXECUTED",
        "package_install": "NOT_EXECUTED",
        "model_weights_in_artifact": "FORBIDDEN",
        "organizational_or_private_data": "NONE",
        "file_digests": [],
        "status": "BLOCKED",
        "temporary_model_bytes": "NOT_RETAINED_ON_NORMAL_EXIT",
    }
    try:
        check_one_shot()
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise RuntimeError("UNSAFE_MANIFEST")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validation = validate_manifest(manifest)
        if validation["allowlisted_files"] != 11 or validation["independently_published_sha256_count"] != 3:
            raise RuntimeError("MANIFEST_EXPECTATIONS_FAILED")
        with tempfile.TemporaryDirectory(prefix="qwen17b-public-one-shot-") as tmp:
            # Absolutely no weights are written to the repository workspace.
            root = pathlib.Path(tmp)
            for entry in manifest["required_files"]:
                receipt["file_digests"].append(locked.download_one(root, entry))
            if len(receipt["file_digests"]) != 11:
                raise RuntimeError("INCOMPLETE_ALLOWLIST")
        receipt["temporary_model_bytes"] = "DELETED_ON_NORMAL_EXIT"
        receipt["status"] = "PASS_11_FILES_3_PUBLISHED_SHA_MATCH_8_SHA_RECORDED"
        return receipt, 0
    except (RuntimeError, ValueError, OSError, KeyError, TypeError,
            json.JSONDecodeError) as err:
        # Do not publish untrusted URL, stderr, secrets, environment values.
        reason = str(err)
        fixed_codes = {
            "UNSAFE_MANIFEST", "MANIFEST_EXPECTATIONS_FAILED",
            "INCOMPLETE_ALLOWLIST", "UNAUTHORIZED_RUNNER_CONTEXT",
            "NOT_GITHUB_HOSTED_RUNNER", "INSUFFICIENT_TEMP_DISK",
            "CURL_NOT_FOUND",
        }
        if reason.startswith("ONE_SHOT_CONTEXT_DENIED_") and reason.removeprefix("ONE_SHOT_CONTEXT_DENIED_") in {
            "GITHUB_WORKFLOW_REF", "GITHUB_RUN_NUMBER", "GITHUB_RUN_ATTEMPT", "GITHUB_JOB"
        }:
            receipt["reason_code"] = reason
        elif reason in fixed_codes:
            receipt["reason_code"] = reason
        elif reason.startswith((
            "HTTPS_DOWNLOAD_FAILED_", "FILE_MISSING_OR_SYMLINK_",
            "EMPTY_FILE_", "FILE_SIZE_MISMATCH_", "FILE_TOO_LARGE_",
            "PUBLISHED_SHA256_MISMATCH_", "DOWNLOAD_TIMEOUT",
        )):
            receipt["reason_code"] = "FILE_ACQUISITION_OR_CHECKSUM_FAILURE"
        else:
            receipt["reason_code"] = "VALIDATION_OR_RUNNER_FAILURE"
        return receipt, 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=pathlib.Path, required=True)
    p.add_argument("--receipt", type=pathlib.Path, required=True)
    args = p.parse_args()
    result, code = acquire(args.manifest)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print("STATUS:", result["status"])
    print("FILES_PROCESSED:", len(result["file_digests"]))
    print("MODEL_INFERENCE:", result["model_inference"])
    print("TEMPORARY_WEIGHTS:", result["temporary_model_bytes"])
    print("REASON_CODE:", result.get("reason_code", "NONE"))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
