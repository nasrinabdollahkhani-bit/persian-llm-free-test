#!/usr/bin/env python3
"""Prepared corrected-retry staging for 11 prior-SHA-verified PUBLIC files. No model in code."""
import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from qwen3_17b_metadata_gate import MODEL, REV, FILES, validate_manifest
from qwen3_17b_acquisition_PREPARED_LOCKED import download_one

def verify_context():
    expected_env = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_REPOSITORY": "nasrinabdollahkhani-bit/persian-llm-free-test",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_ACTOR": "nasrinabdollahkhani-bit",
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "GITHUB_RUN_NUMBER": "1",
        "GITHUB_RUN_ATTEMPT": "1",
        "GITHUB_WORKFLOW_REF": "nasrinabdollahkhani-bit/persian-llm-free-test/.github/workflows/qwen3-17b-farsi-inference-retry-r1.yml@refs/heads/main",
        "GITHUB_JOB": "persian10", "RUNNER_OS": "Linux"
    }
    if any(os.environ.get(k) != v for k,v in expected_env.items()):
        raise RuntimeError("ONE_SHOT_CONTEXT_DENIED")


def validate_hash_lock(manifest, lock):
    validate_manifest(manifest)
    if lock["source_run_id"] != "38734778931" or lock["fixed_revision"] != "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e":
        raise RuntimeError("PRIOR_RECEIPT_IDENTITY_MISMATCH")
    hashes=lock["sha256"]
    if set(hashes)!=set(FILES) or len(hashes)!=11:
        raise RuntimeError("ALLOWLIST_MISMATCH")
    for entry in manifest["required_files"]:
        if entry["sha256"] and entry["sha256"]!=hashes[entry["name"]]:
            raise RuntimeError("PUBLISHED_SHA_CONFLICT")


def stage(root, manifest_path, lock_path):
    receipt={"model":MODEL,"revision":REV,"prior_run":"38734778931","status":"BLOCKED",
             "inference":"NOT_EXECUTED","file_digests":[]}
    verify_context()
    if root.is_symlink():
        raise RuntimeError("UNSAFE_MODEL_DIR")
    root = root.resolve(strict=True)
    if not root.is_dir() or any(root.iterdir()):
        raise RuntimeError("UNSAFE_MODEL_DIR")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    validate_hash_lock(manifest,lock)
    hashes=lock["sha256"]
    for entry in manifest["required_files"]:
        row = download_one(root, entry)
        if row["sha256_received"] != hashes[entry["name"]]:
            raise RuntimeError("PREVIOUS_RECEIPT_SHA_MISMATCH")
        row["matches_prior_receipt"] = True
        receipt["file_digests"].append(row)
    receipt["status"] = "STAGED_11_OF_11_PREVIOUS_SHA_MATCH"
    return receipt

def main():
    p=argparse.ArgumentParser()
    for arg in ("model-dir", "manifest", "sha-lock", "receipt"):
        p.add_argument("--"+arg, type=Path, required=True)
    a=p.parse_args()
    receipt=stage(a.model_dir,a.manifest,a.sha_lock)
    a.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("STAGING_STATUS:",receipt["status"],"FILES:",len(receipt["file_digests"]))

if __name__ == "__main__":
    main()
