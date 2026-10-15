#!/usr/bin/env python3
"""One CPU-only run: 10 raw synthetic Persian responses, never product acceptance."""
import argparse
import json
import os
import pathlib
import resource
import sys
import time
from datetime import datetime, timezone

from qwen_farsi_quality_v2 import (
    PROMPTS, SYSTEM, EXAMPLE, SEED, GENERATION,
    build_messages, observable_only, sha256_file,
)

MODEL = "Qwen/Qwen3-1.7B"
REV = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"
PROFILE = "QWEN3_17B_FA10_V2_COMPARABLE_NONTHINKING"
EXPECTED_BASELINE = "38711873242"


def preverify(root, lock_path):
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError("MODEL_ROOT_UNSAFE")
    root = root.resolve(strict=True)
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock.get("fixed_revision") != REV or lock.get("model_repo") != MODEL:
        raise RuntimeError("MODEL_REVISION_MISMATCH")
    digests = lock["sha256"]
    if len(digests) != 11 or set(digests) != {p.name for p in root.iterdir()}:
        raise RuntimeError("MODEL_FILE_SET_MISMATCH")
    for name, expected in digests.items():
        f = root / name
        if f.is_symlink() or not f.is_file() or f.resolve().parent != root:
            raise RuntimeError("UNSAFE_MODEL_FILE")
        if sha256_file(f) != expected:
            raise RuntimeError("MODEL_SHA256_MISMATCH")
    return digests


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model-dir", type=pathlib.Path, required=True)
    p.add_argument("--sha-lock", type=pathlib.Path, required=True)
    p.add_argument("--output", type=pathlib.Path, required=True)
    args = p.parse_args()
    os.environ.update({
        "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
        "HF_DATASETS_OFFLINE": "1", "HF_HUB_DISABLE_TELEMETRY": "1",
        "TOKENIZERS_PARALLELISM": "false", "CUDA_VISIBLE_DEVICES": "",
    })
    verified = preverify(args.model_dir, args.sha_lock)
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if torch.version.cuda is not None or torch.cuda.is_available():
        raise RuntimeError("CPU_ONLY_CONTRACT")
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    root = args.model_dir.resolve(strict=True)
    tokenizer = AutoTokenizer.from_pretrained(
        str(root), local_files_only=True, trust_remote_code=False, use_fast=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        str(root), local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.float32
    )
    model.eval()
    report = {
        "schema": "morteza5.public.qwen3-1.7b.synthetic-persian-ten.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL, "immutable_revision": REV,
        "prior_verified_acquisition_run": "38734778931",
        "reference_quality_v2_run": EXPECTED_BASELINE,
        "profile": PROFILE,
        "prompt_contract": "all_10_prompts_exactly_equal_to_prior_qwen3_0.6b_v2",
        "system_message": SYSTEM, "example_messages": list(EXAMPLE),
        "generation_parameters": dict(GENERATION), "thinking": False,
        "verified_all_11_sha256": verified,
        "torch": torch.__version__, "transformers": transformers.__version__,
        "required_count": 10, "actual_count": 0,
        "answers": [], "technical_status": "IN_PROGRESS",
        "semantic_quality": "NOT_AUTOMATICALLY_EVALUATED_HUMAN_REVIEW_REQUIRED",
        "apex_connection": "NONE", "organizational_data": "NONE",
        "windows_security": "NOT_EXECUTED",
    }

    def save():
        report["max_rss_kib_linux"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save()
    for i, question in enumerate(PROMPTS, start=1):
        formatted = tokenizer.apply_chat_template(
            build_messages(question), tokenize=False,
            add_generation_prompt=True, enable_thinking=False,
        )
        inp = tokenizer(formatted, return_tensors="pt")
        torch.manual_seed(SEED + i)
        start = time.monotonic()
        with torch.inference_mode():
            tokens = model.generate(
                **inp, **GENERATION,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
            )
        seconds = round(time.monotonic() - start, 3)
        new_tokens = tokens[0][inp.input_ids.shape[-1]:]
        n = int(new_tokens.numel())
        answer = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        reason = "EOS" if n and int(new_tokens[-1]) == tokenizer.eos_token_id else (
            "MAX_NEW_TOKENS" if n >= GENERATION["max_new_tokens"] else "OTHER"
        )
        report["answers"].append({
            "index": i, "prompt": question,
            "baseline_prompt_unchanged": True,
            "raw_model_response": answer, "generated_token_count": n,
            "elapsed_seconds": seconds, "seed": SEED + i,
            "stop_reason": reason,
            "observable_diagnostics_not_quality_score": observable_only(answer),
        })
        report["actual_count"] = len(report["answers"])
        save()
        print("RAW_PERSIAN_RESPONSE:", i, "/10", "TOKENS:", n, "SECONDS:", seconds, flush=True)
    report["technical_status"] = (
        "TEN_RAW_RESPONSES_GENERATED" if len(report["answers"]) == 10
        and all(x["raw_model_response"] for x in report["answers"])
        else "INCOMPLETE_OR_EMPTY_RESPONSES"
    )
    save()
    if report["technical_status"] != "TEN_RAW_RESPONSES_GENERATED":
        raise RuntimeError("INCOMPLETE_OR_EMPTY_RESPONSES")
    print("TEN_REAL_MODEL_RESPONSES: 10/10; HUMAN_PERSIAN_QUALITY_REVIEW_REQUIRED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FA10_INFERENCE_FAILURE_CLASS:", type(exc).__name__, file=sys.stderr)
        raise SystemExit(2)
