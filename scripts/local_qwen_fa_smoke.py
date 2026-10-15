#!/usr/bin/env python3
"""Prepared, UNTRIGGERED offline-only text smoke test for one locally staged model.

NO download routine, no package installation, no CI workflow invocation, no corporate data.
Requires separate authorizations and independently verified model/runtime before use.
Do not publish private or organizational inputs/outputs in a public repository.
"""
import argparse
import hashlib
import json
import os
import pathlib
import resource
import sys
import time
from datetime import datetime, timezone

# Published upstream digests; must be independently matched to received file bytes.
EXPECTED_SHA256 = {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b",
    "tokenizer.json": "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4",
}
REQUIRED_FILES = (
    "model.safetensors", "tokenizer.json", "tokenizer_config.json",
    "config.json", "generation_config.json", "LICENSE", "README.md",
)
PROMPTS = (
    "سلام! خودت را در یک جمله فارسی معرفی کن.",
    "اگر به داده های واقعی دسترسی نداری، چگونه درباره آمار پاسخ می دهی؟",
    "بدون ساختن عدد یا ادعای دسترسی به داده، فایده مقایسه دو استان را توضیح بده.",
    "سه معیار کوتاه برای ارزیابی کیفیت پاسخ فارسی نام ببر.",
    "اگر پرسش کاربر مبهم باشد، بهترین اقدام چیست؟",
)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_model_dir(model_dir):
    root = model_dir.resolve(strict=True)
    for name in REQUIRED_FILES:
        p = root / name
        if not p.is_file() or p.is_symlink() or p.resolve().parent != root:
            raise RuntimeError(f"MISSING_OR_UNSAFE_FILE:{name}")
    actual = {name: sha256(root / name) for name in EXPECTED_SHA256}
    for name, expected in EXPECTED_SHA256.items():
        if actual[name] != expected:
            raise RuntimeError(f"SHA256_MISMATCH:{name}")
    return root, actual


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=pathlib.Path, required=True)
    ap.add_argument("--output", type=pathlib.Path, default=pathlib.Path("five_public_synthetic_responses.json"))
    ap.add_argument("--max-new-tokens", type=int, default=80)
    args = ap.parse_args()

    if args.max_new_tokens < 1 or args.max_new_tokens > 120:
        raise RuntimeError("TOKEN_BUDGET_OUT_OF_RANGE")
    root, digests = verify_model_dir(args.model_dir)
    # Enforce local files only at the HF/Transformers API boundary.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(min(4, os.cpu_count() or 1))
    tokenizer = AutoTokenizer.from_pretrained(str(root), local_files_only=True, trust_remote_code=False, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(root),
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype=torch.float32,
    )
    model.eval()
    answers = []
    for idx, prompt in enumerate(PROMPTS, 1):
        messages = [
            {"role": "system", "content": "فقط بر اساس پرسش جواب بده. به اطلاعات بیرونی یا داده سازمانی دسترسی نداری. پاسخ کوتاه و فارسی باشد."},
            {"role": "user", "content": prompt},
        ]
        formatted = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
        inputs = tokenizer(formatted, return_tensors="pt")
        started = time.monotonic()
        with torch.inference_mode():
            result = model.generate(
                **inputs, max_new_tokens=args.max_new_tokens, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        seconds = round(time.monotonic() - started, 3)
        response = tokenizer.decode(result[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()
        answers.append({
            "index": idx, "prompt": prompt, "raw_model_response": response,
            "generated_token_count": int(result.shape[-1] - inputs.input_ids.shape[-1]),
            "elapsed_seconds": seconds,
        })
    report = {
        "schema": "public.synthetic.persian-text-smoke.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_model_only": True,
        "network_isolation_independently_proven": False,
        "upstream_sha256_verified_against_received_bytes": digests,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "answers": answers,
        "llm_text_smoke": "COMPLETED_WITH_RAW_OUTPUT_NOT_INDEPENDENTLY_AUDITED",
        "stt": "NOT_EXECUTED", "tts": "NOT_EXECUTED", "windows_native": "NOT_EXECUTED",
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"result": report["llm_text_smoke"], "answers_count": len(answers), "report": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"BLOCKED_OR_FAILED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
