#!/usr/bin/env python3
"""Strictly metadata-only readiness check for a pinned public model candidate.

NO network calls; NO model weight acquisition; NO inference; stdlib only.
A PASS is a provenance/config + *estimated* capacity check, never authorization.
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import tempfile
from datetime import datetime, timezone

REV = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"
MODEL = "Qwen/Qwen3-1.7B"
FILES = (
    "LICENSE", "README.md", "config.json", "generation_config.json",
    "merges.txt", "model-00001-of-00002.safetensors",
    "model-00002-of-00002.safetensors", "model.safetensors.index.json",
    "tokenizer.json", "tokenizer_config.json", "vocab.json",
)
SHA = {
    "model-00001-of-00002.safetensors":
        "169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5",
    "model-00002-of-00002.safetensors":
        "912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9",
    "tokenizer.json":
        "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4",
}
INDEX_TENSOR_SIZE = 4063479808
SHARD_FILE_TOTAL = 4063515592
NAME = "qwen3_17b_metadata_gate_receipt.json"


def validate_manifest(m):
    if m.get("model_repo") != MODEL or m.get("fixed_revision") != REV:
        raise ValueError("WRONG_MODEL_OR_REVISION")
    if not re.fullmatch(r"[0-9a-f]{40}", m["fixed_revision"]):
        raise ValueError("NON_IMMUTABLE_REVISION")
    entries = m.get("required_files", [])
    if len(entries) != len(FILES) or tuple(x.get("name") for x in entries) != FILES:
        raise ValueError("ALLOWLIST_DIFFERENCE")
    if m.get("index_reported_tensor_bytes") != INDEX_TENSOR_SIZE:
        raise ValueError("INDEX_TENSOR_SIZE_MISMATCH")
    if m.get("published_shards_total_file_bytes") != SHARD_FILE_TOTAL:
        raise ValueError("SHARD_FILE_TOTAL_MISMATCH")
    weights = 0
    for entry in entries:
        name = entry["name"]
        if not re.fullmatch(r"[a-zA-Z0-9._-]+", name) or name.startswith("."):
            raise ValueError("UNSAFE_FILE_NAME")
        expected = SHA.get(name)
        if expected:
            if entry.get("sha256") != expected or not re.fullmatch(r"[a-f0-9]{64}", entry["sha256"]):
                raise ValueError("PUBLISHED_SHA_MISMATCH")
        elif entry.get("sha256") is not None:
            raise ValueError("UNVERIFIED_SHA_PRETENDED_PUBLISHED")
        if name.endswith(".safetensors"):
            weights += entry.get("bytes", 0)
    if weights != SHARD_FILE_TOTAL:
        raise ValueError("SUM_OF_WEIGHT_SHARDS_MISMATCH")
    a = m.get("authorization", {})
    if a.get("model_acquisition") != "NOT_AUTHORIZED_BY_THIS_MANIFEST":
        raise ValueError("ACQUISITION_AUTHORIZATION_SCOPE_VIOLATION")
    if a.get("model_inference") != "NOT_AUTHORIZED":
        raise ValueError("INFERENCE_AUTHORIZATION_SCOPE_VIOLATION")
    if a.get("paid_runners") != "FORBIDDEN" or a.get("org_data") != "FORBIDDEN":
        raise ValueError("BOUNDARY_VIOLATION")
    return {"allowlisted_files": len(FILES),
            "independently_published_sha256_count": len(SHA),
            "published_shard_file_bytes": weights,
            "index_reported_tensor_bytes": INDEX_TENSOR_SIZE,
            "license_declared": m.get("license_declared"),
            "legal_review": m.get("organization_legal_review")}


def linux_memory():
    vals = {}
    p = pathlib.Path("/proc/meminfo")
    if not p.exists():
        return 0, 0
    for line in p.read_text(encoding="utf-8").splitlines():
        left, _, right = line.partition(":")
        if left in ("MemTotal", "MemAvailable"):
            vals[left] = int(right.strip().split()[0]) * 1024
    return vals.get("MemTotal", 0), vals.get("MemAvailable", 0)


def capacity_snapshot():
    cpus = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else (os.cpu_count() or 0)
    total, available = linux_memory()
    disk = shutil.disk_usage(tempfile.gettempdir()).free
    # A prospective storage/capacity advisory, NOT empirical model-fit evidence.
    return {
        "cpu_affinity": cpus,
        "ram_total_bytes": total,
        "ram_available_bytes": available,
        "temporary_disk_free_bytes": disk,
        "capacity_minimums_met": (cpus >= 4 and total >= 14 * 1024**3 and disk >= 12 * 1024**3),
        "model_runtime_memory_fit_proven": False,
    }


def check_github_context():
    if os.getenv("GITHUB_ACTIONS") != "true":
        return "LOCAL_METADATA_INSPECTION_ONLY"
    required = {
        "GITHUB_REPOSITORY": "nasrinabdollahkhani-bit/persian-llm-free-test",
        "GITHUB_ACTOR": "nasrinabdollahkhani-bit",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "RUNNER_OS": "Linux",
    }
    if any(os.environ.get(k) != v for k, v in required.items()):
        raise ValueError("UNAUTHORIZED_GITHUB_CONTEXT")
    return "AUTHORIZED_PUBLIC_REPO_METADATA_ONLY"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=pathlib.Path)
    parser.add_argument("--output", default=NAME, type=pathlib.Path)
    args = parser.parse_args()
    report = {
        "schema": "morteza5.qwen3-17b.metadata-gate-receipt.v1",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "model_repo": MODEL, "immutable_revision": REV,
        "model_download": "NOT_EXECUTED", "model_inference": "NOT_EXECUTED",
        "package_install": "NOT_EXECUTED", "windows_native": "NOT_EXECUTED",
        "weights_as_artifacts": "FORBIDDEN",
        "acquisition_owner_signed_authorization": "NOT_PROVIDED_OR_VERIFIED",
        "inference_owner_signed_authorization": "NOT_PROVIDED_OR_VERIFIED",
        "metadata_verdict": "BLOCKED",
    }
    code = 2
    try:
        report["environment"] = check_github_context()
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report.update(validate_manifest(manifest))
        report.update(capacity_snapshot())
        report["metadata_verdict"] = "METADATA_MANIFEST_VERIFIED"
        report["capacity_verdict"] = (
            "PROVISIONAL_CAPACITY_MINIMUMS_MET_NOT_MODEL_FIT"
            if report["capacity_minimums_met"] else "CAPACITY_MINIMUMS_NOT_MET"
        )
        code = 0 if report["capacity_minimums_met"] else 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        report["reason_code"] = type(exc).__name__
    finally:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("MODEL_DOWNLOAD:", report["model_download"])
        print("MODEL_INFERENCE:", report["model_inference"])
        print("METADATA_VERDICT:", report["metadata_verdict"])
        print("CAPACITY_VERDICT:", report.get("capacity_verdict", "NOT_CHECKED"))
        if report.get("reason_code"):
            print("FAILURE_CLASS:", report["reason_code"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
