#!/usr/bin/env python3
"""Qwen3-1.7B acquisition PREPARATION, HARD LOCKED, 2026-10-15.

NO DOWNLOAD IS POSSIBLE IN THIS COMMITTED VERSION. The individual project
owner must explicitly approve the single public-model download in this chat;
a separately reviewed code change must then activate the acquisition gate. This program is NOT a runner
workflow. No model imports, no pip packages, no inference, no private data.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

from qwen3_17b_metadata_gate import MODEL, REV, FILES, SHA, validate_manifest

# Must remain FALSE until explicit chat approval by the personal project
# owner AND a separately reviewed code change. No CLI/environment variable
# or workflow input may override the current source-level lock.
ACQUISITION_ENABLED = False
RECEIPT_FILE = "qwen3_17b_acquisition_sha_only_receipt.json"
MODEL_SHARD_MAX_BYTES = 4 * 1024**3
SMALL_FILE_MAX_BYTES = 32 * 1024**2
MIN_DISK_FREE_BYTES = 12 * 1024**3


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for buf in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(buf)
    return h.hexdigest()


def verify_context():
    require = {
        "GITHUB_REPOSITORY": "nasrinabdollahkhani-bit/persian-llm-free-test",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_ACTOR": "nasrinabdollahkhani-bit",
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "RUNNER_OS": "Linux",
    }
    if any(os.environ.get(k) != v for k, v in require.items()):
        raise RuntimeError("UNAUTHORIZED_RUNNER_CONTEXT")
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("NOT_GITHUB_HOSTED_RUNNER")
    if shutil.disk_usage(tempfile.gettempdir()).free < MIN_DISK_FREE_BYTES:
        raise RuntimeError("INSUFFICIENT_TEMP_DISK")
    if not shutil.which("curl"):
        raise RuntimeError("CURL_NOT_FOUND")


def assert_acquisition_authorized():
    # This happens before any network or file download.
    if not ACQUISITION_ENABLED:
        raise RuntimeError("STOP_NO_EXPLICIT_OWNER_CHAT_CONSENT")


def download_one(root, entry):
    name = entry["name"]
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name) or name.startswith(".") or name not in FILES:
        raise RuntimeError("DISALLOWED_MODEL_FILENAME")
    target = root / name
    url = f"https://huggingface.co/{MODEL}/resolve/{REV}/{name}"
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--proto", "=https", "--proto-redir", "=https",
        "--max-redirs", "8", "--connect-timeout", "30", "--retry", "2",
        "--retry-delay", "2", "--max-time", "1800", "--output",
        str(target), url,
    ]
    try:
        result = subprocess.run(command, check=False, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=1850)
    except subprocess.TimeoutExpired:
        raise RuntimeError("DOWNLOAD_TIMEOUT") from None
    if result.returncode != 0:
        raise RuntimeError("HTTPS_DOWNLOAD_FAILED_" + name)
    if not target.is_file() or target.is_symlink():
        raise RuntimeError("FILE_MISSING_OR_SYMLINK_" + name)
    size = target.stat().st_size
    if size <= 0:
        raise RuntimeError("EMPTY_FILE_" + name)
    expected_size = entry.get("bytes")
    if expected_size is not None and size != expected_size:
        raise RuntimeError("FILE_SIZE_MISMATCH_" + name)
    cap = MODEL_SHARD_MAX_BYTES if name.endswith(".safetensors") else SMALL_FILE_MAX_BYTES
    if size > cap:
        raise RuntimeError("FILE_TOO_LARGE_" + name)
    actual = sha256(target)
    expected_hash = SHA.get(name)
    if expected_hash is not None and actual != expected_hash:
        raise RuntimeError("PUBLISHED_SHA256_MISMATCH_" + name)
    return {
        "public_filename": name,
        "bytes_received": size,
        "sha256_received": actual,
        "published_sha256": expected_hash,
        "verification": (
            "MATCH_PUBLIC_UPSTREAM_SHA256" if expected_hash
            else "CALCULATED_AT_PINNED_COMMIT_UPSTREAM_HASH_NOT_INDEPENDENTLY_PUBLISHED"
        ),
    }


def run(manifest_path):
    report = {
        "schema": "morteza5.public.qwen3-17b.acquisition-only.v1",
        "model": MODEL,
        "immutable_revision": REV,
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "owner_acquisition_chat_consent": "NOT_VERIFIED_BY_THIS_SCRIPT",
        "model_execution": "NOT_EXECUTED",
        "packages_installed": "NOT_EXECUTED",
        "windows_native": "NOT_EXECUTED",
        "organizational_data": "NONE",
        "model_bytes_uploaded": False,
        "status": "BLOCKED",
        "file_digests": [],
    }
    try:
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise RuntimeError("UNSAFE_MANIFEST")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_manifest(manifest)
        verify_context()
        assert_acquisition_authorized()
        with tempfile.TemporaryDirectory(prefix="qwen17b-public-acquisition-") as temp:
            root = pathlib.Path(temp)
            for entry in manifest["required_files"]:
                report["file_digests"].append(download_one(root, entry))
        report["status"] = "ALL_11_RECEIVED_3_UPSTREAM_SHA_MATCH_OTHER_8_CALCULATED"
        return report, 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, json.JSONDecodeError) as e:
        # Do not put untrusted stderr, URLs, file content or tokens into public receipt.
        safe_codes = {
            "UNSAFE_MANIFEST", "UNAUTHORIZED_RUNNER_CONTEXT",
            "NOT_GITHUB_HOSTED_RUNNER", "INSUFFICIENT_TEMP_DISK",
            "CURL_NOT_FOUND", "STOP_NO_EXPLICIT_OWNER_CHAT_CONSENT",
            "DOWNLOAD_TIMEOUT",
        }
        code = str(e)
        if code in safe_codes or re.fullmatch(
            r"(?:HTTPS_DOWNLOAD_FAILED|FILE_MISSING_OR_SYMLINK|EMPTY_FILE|"
            r"FILE_SIZE_MISMATCH|FILE_TOO_LARGE|PUBLISHED_SHA256_MISMATCH)_"
            r"[A-Za-z0-9._-]+", code
        ):
            report["reason_code"] = code
        else:
            report["reason_code"] = "UNEXPECTED_VALIDATION_ERROR"
        return report, 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--receipt", type=pathlib.Path, default=pathlib.Path(RECEIPT_FILE))
    args = parser.parse_args()
    report, rc = run(args.manifest)
    args.receipt.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("DOWNLOAD_STATUS:", report["status"])
    print("FILE_DIGEST_RECORDS:", len(report["file_digests"]))
    print("MODEL_EXECUTION:", report["model_execution"])
    print("REASON_CODE:", report.get("reason_code", "NONE"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
