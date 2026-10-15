#!/usr/bin/env python3
"""Stage exactly seven public Qwen files on an ephemeral GitHub runner.

All received SHA-256 values must match the prior authorized acquisition run.
This script stages local assets ONLY; it does not import or run a model.
"""
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

from qwen_acquisition_only import FILES, HF_REPO, REV, check_context, one_file

PREVIOUS_RUN = "38678468114"
PINNED_SHA256 = {
    "LICENSE": "832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e",
    "README.md": "1ab64a26fcb3b461423b89a433a8c858f1bf8d4086f979cbb3ff878d47cf20e9",
    "config.json": "660db3b73d788119c04535e48cf9be5f55bc3100841a718637ae695b442f27dd",
    "generation_config.json": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "tokenizer_config.json": "d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101",
    "tokenizer.json": "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4",
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b",
}
EXPECTED_FILE_NAMES = tuple(name for name, _, _ in FILES)
RECEIPT = pathlib.Path("five_response_model_stage_receipt.json")


def main():
    report = {
        "schema": "public.synthetic.qwen-model-stage.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "authorized_prior_run": PREVIOUS_RUN,
        "model_repository": HF_REPO,
        "revision": REV,
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "status": "BLOCKED",
        "inference": "NOT_EXECUTED_BY_STAGE",
        "file_digests": [],
    }
    try:
        check_context()
        if len(sys.argv) != 2:
            raise RuntimeError("EXACTLY_ONE_MODEL_DIRECTORY_REQUIRED")
        root = pathlib.Path(sys.argv[1]).resolve(strict=True)
        if not root.is_dir() or root.is_symlink():
            raise RuntimeError("UNSAFE_MODEL_DIRECTORY")
        if set(PINNED_SHA256) != set(EXPECTED_FILE_NAMES) or len(FILES) != 7:
            raise RuntimeError("FILE_ALLOWLIST_INCONSISTENT")
        for name, expected_size, expected_published in FILES:
            result = one_file(root, name, expected_size, expected_published)
            if result["received_sha256"] != PINNED_SHA256[name]:
                raise RuntimeError("PREVIOUS_RECEIPT_SHA_MISMATCH:" + name)
            result["matching_prior_acquisition_receipt_sha256"] = True
            report["file_digests"].append(result)
        report["status"] = "STAGED_7_OF_7_SHA_VERIFIED"
        return 0
    except Exception as exc:
        # Do not echo untrusted text or potentially secret URL values to public logs.
        report["reason_code"] = (
            str(exc) if isinstance(exc, RuntimeError) and str(exc).split(":", 1)[0] in {
                "DISALLOWED_EXECUTION_CONTEXT", "EXACTLY_ONE_MODEL_DIRECTORY_REQUIRED",
                "UNSAFE_MODEL_DIRECTORY", "FILE_ALLOWLIST_INCONSISTENT",
                "PREVIOUS_RECEIPT_SHA_MISMATCH", "UPSTREAM_SHA256_MISMATCH",
                "UPSTREAM_SIZE_MISMATCH", "DOWNLOAD_FAILED", "MISSING_DOWNLOADED_FILE",
                "UNEXPECTED_SIZE", "INSUFFICIENT_TEMP_DISK", "CURL_NOT_INSTALLED"
            } else "STAGING_FAILURE"
        )
        return 2
    finally:
        RECEIPT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("STAGING_STATUS:", report["status"])
        print("FILES_HASHED:", len(report["file_digests"]))
        print("MODEL_EXECUTED_BY_STAGE:", report["inference"])
        if report.get("reason_code"):
            print("FAILURE_REASON:", report["reason_code"])


if __name__ == "__main__":
    raise SystemExit(main())
