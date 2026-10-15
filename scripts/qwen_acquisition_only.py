#!/usr/bin/env python3
"""One-shot, strictly acquisition-only Qwen3-0.6B provenance gate.

Authorized: exactly 7 public files at one immutable HF revision, on a temporary
GitHub-hosted free standard runner. Never imports ML frameworks or executes a model.
No weights, raw model bytes, secrets or private files enter GitHub artifacts.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REPO = "nasrinabdollahkhani-bit/persian-llm-free-test"
REV = "c1899de289a04d12100db370d81485cdf75e47ca"
HF_REPO = "Qwen/Qwen3-0.6B"
FILES = (
    ("LICENSE", None, None),
    ("README.md", None, None),
    ("config.json", None, None),
    ("generation_config.json", None, None),
    ("tokenizer_config.json", None, None),
    ("tokenizer.json", 11422654, "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4"),
    ("model.safetensors", 1503300328, "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"),
)
RECEIPT_NAME = "qwen_acquisition_receipt.json"
MAX_SMALL = 16 * 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_context():
    required = {
        "GITHUB_REPOSITORY": REPO,
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_ACTOR": "nasrinabdollahkhani-bit",
        "RUNNER_OS": "Linux",
    }
    for key, expected in required.items():
        if os.environ.get(key) != expected:
            raise RuntimeError("DISALLOWED_EXECUTION_CONTEXT:" + key)
    if shutil.which("curl") is None:
        raise RuntimeError("CURL_NOT_INSTALLED")
    if shutil.disk_usage(tempfile.gettempdir()).free < 3 * 1024**3:
        raise RuntimeError("INSUFFICIENT_TEMP_DISK")


def one_file(dest, name, expected_size, expected_hash):
    if "/" in name or "\\" in name or name.startswith("."):
        raise RuntimeError("INVALID_ALLOWLIST_NAME")
    url = f"https://huggingface.co/{HF_REPO}/resolve/{REV}/{name}"
    target = dest / name
    result = subprocess.run(
        [
            "curl", "--fail", "--location", "--silent", "--show-error",
            "--proto", "=https", "--proto-redir", "=https",
            "--max-redirs", "8", "--connect-timeout", "30",
            "--max-time", "1200", "--retry", "2", "--retry-delay", "2",
            "--output", str(target), url,
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=1250,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"DOWNLOAD_FAILED:{name}:CURL_EXIT_{result.returncode}")
    if not target.is_file() or target.is_symlink():
        raise RuntimeError("MISSING_DOWNLOADED_FILE:" + name)
    n = target.stat().st_size
    if n == 0 or n > (1700000000 if name == "model.safetensors" else MAX_SMALL):
        raise RuntimeError("UNEXPECTED_SIZE:" + name)
    if expected_size is not None and n != expected_size:
        raise RuntimeError("UPSTREAM_SIZE_MISMATCH:" + name)
    actual = digest(target)
    if expected_hash is not None and actual.lower() != expected_hash.lower():
        raise RuntimeError("UPSTREAM_SHA256_MISMATCH:" + name)
    return {
        "name": name, "received_bytes": n, "received_sha256": actual,
        "expected_upstream_sha256": expected_hash,
        "digest_verdict": "MATCH_PUBLISHED_SHA256" if expected_hash else "CALCULATED_PINNED_REVISION_ONLY",
    }


def main():
    report = {
        "schema": "morteza5.tamin.qwen-acquisition-only.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "repository": REPO,
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "model_repository": HF_REPO,
        "pinned_revision": REV,
        "authorized_files": [item[0] for item in FILES],
        "report_visibility": "PUBLIC_METADATA_ONLY",
        "model_inference": "NOT_EXECUTED",
        "runtime_packages_installed": False,
        "windows_native": "NOT_EXECUTED",
        "apex_or_mother_access": "NONE",
        "weights_uploaded_as_artifact": False,
        "acquisition_verdict": "BLOCKED",
        "file_digests": [],
    }
    try:
        check_context()
        with tempfile.TemporaryDirectory(prefix="qwen3-acquisition-only-") as dirname:
            root = pathlib.Path(dirname)
            for name, size, expected in FILES:
                # Only public upstream model files. No model import or inference.
                report["file_digests"].append(one_file(root, name, size, expected))
        report["acquisition_verdict"] = "SHA_VERIFIED_TWO_UPSTREAM_AND_SEVEN_RECEIVED"
        return_code = 0
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        # Never leak curl redirect URLs/tokens or file contents into public logs.
        code = str(exc).split("\n", 1)[0][:150]
        report["reason_code"] = code
        return_code = 2
    finally:
        pathlib.Path(RECEIPT_NAME).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("QWEN_ACQUISITION_VERDICT:", report["acquisition_verdict"])
        print("FILES_RECEIVED_AND_HASHED:", len(report["file_digests"]))
        print("MODEL_INFERENCE:", report["model_inference"])
        if "reason_code" in report:
            print("REASON_CODE:", report["reason_code"])
        print("PUBLIC_RECEIPT:", RECEIPT_NAME)
    return return_code


if __name__ == "__main__":
    sys.exit(main())
