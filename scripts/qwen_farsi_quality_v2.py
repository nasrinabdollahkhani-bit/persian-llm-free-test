#!/usr/bin/env python3
"""Public synthetic-only Persian quality experiment, v2. NOT a product gate.

This program ONLY reads the previously verified local seven-file Qwen directory.
No downloads, no package installation, no APEX/Mother/org input, no network API.
Raw model text is retained unmodified. Quality requires independent human review.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import resource
import sys
import time
from datetime import datetime, timezone

SCHEMA = "public.synthetic.qwen3-persian-quality-v2"
PROFILE = "FA_QUALITY_V2_NONTHINKING_SAMPLING"
SEED = 20261015
MAX_NEW_TOKENS = 160
EXPECTED_SHA256 = {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b",
    "tokenizer.json": "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4",
    "LICENSE": "832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e",
    "README.md": "1ab64a26fcb3b461423b89a433a8c858f1bf8d4086f979cbb3ff878d47cf20e9",
    "config.json": "660db3b73d788119c04535e48cf9be5f55bc3100841a718637ae695b442f27dd",
    "generation_config.json": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "tokenizer_config.json": "d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101",
}
# The first five prompts are BYTE-FOR-BYTE the same as baseline run 38685295846.
PROMPTS = (
    "سلام! خودت را در یک جمله فارسی معرفی کن.",
    "اگر به داده های واقعی دسترسی نداری، چگونه درباره آمار پاسخ می دهی؟",
    "بدون ساختن عدد یا ادعای دسترسی به داده، فایده مقایسه دو استان را توضیح بده.",
    "سه معیار کوتاه برای ارزیابی کیفیت پاسخ فارسی نام ببر.",
    "اگر پرسش کاربر مبهم باشد، بهترین اقدام چیست؟",
    "برای بررسی یک گزارش آماری چه پرسش های تکمیلی باید مطرح شود؟",
    "تفاوت داده معتبر و عدد حدسی را در دو جمله توضیح بده.",
    "چگونه درباره یک موضوع نامطمئن پاسخ مسئولانه می دهی؟",
    "چه راهی برای خلاصه کردن یک گزارش طولانی به فارسی پیشنهاد می کنی؟",
    "برای مقایسه روندها بدون دسترسی به داده واقعی چه احتیاطی لازم است؟",
)
SYSTEM = (
    "تو دستیار آزمایشی فارسی هستی. فقط به فارسی روان و درست بنویس. "
    "به اطلاعات روز، اینترنت، آمار واقعی یا سامانه‌های سازمانی دسترسی نداری. "
    "عدد، منبع یا واقعیت نامعلوم را حدس نزن. اگر داده لازم موجود نیست، روشن بگو "
    "و روش بررسی را پیشنهاد بده. اگر سؤال مبهم است، یک سؤال تکمیلی مشخص بپرس. "
    "برای هر پرسش، یک یا دو جمله کامل و مرتبط بنویس؛ از کلی‌گویی و تکرار خودداری کن."
)
EXAMPLE = (
    {"role": "user", "content": "می‌توانی تعداد دقیق مراجعه‌کنندگان یک مرکز فرضی را بگویی؟"},
    {"role": "assistant", "content": "خیر، به آمار واقعی دسترسی ندارم. برای پاسخ دقیق، نام مرکز و دوره زمانی را مشخص کنید و به گزارش معتبر رجوع کنید."},
)
GENERATION = {
    "do_sample": True,
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "max_new_tokens": MAX_NEW_TOKENS,
}


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for data in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()


def verify_model(root):
    root = root.resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError("MODEL_DIRECTORY_INVALID")
    for name, expected in EXPECTED_SHA256.items():
        p = root / name
        if p.is_symlink() or not p.is_file() or p.resolve().parent != root:
            raise RuntimeError("MISSING_OR_UNSAFE_FILE:" + name)
        if sha256_file(p) != expected:
            raise RuntimeError("SHA256_MISMATCH:" + name)
    return root


def build_messages(prompt):
    return [
        {"role": "system", "content": SYSTEM},
        dict(EXAMPLE[0]),
        dict(EXAMPLE[1]),
        {"role": "user", "content": prompt},
    ]


def observable_only(text):
    """Diagnostics, NOT a semantic quality score or PASS."""
    words = re.findall(r"\S+", text)
    persian_chars = sum(('\u0600' <= ch <= '\u06ff') for ch in text)
    letters = sum(ch.isalpha() for ch in text)
    return {
        "word_count": len(words),
        "persian_codepoint_count": persian_chars,
        "persian_to_alpha_ratio": round(persian_chars / max(1, letters), 3),
        "short_response_flag": len(words) < 6,
        "non_persian_dominance_flag": bool(letters) and persian_chars / letters < 0.5,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--count", type=int, choices=range(5, 11), required=True)
    args = parser.parse_args()

    # Local-only behavior is enforced before importing any model libraries.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    root = verify_model(args.model_dir)

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if torch.cuda.is_available() or torch.version.cuda is not None:
        raise RuntimeError("CPU_ONLY_REQUIRED")
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    tokenizer = AutoTokenizer.from_pretrained(
        str(root), local_files_only=True, trust_remote_code=False, use_fast=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        str(root), local_files_only=True, trust_remote_code=False, torch_dtype=torch.float32
    )
    model.eval()
    outputs = []
    for i, question in enumerate(PROMPTS[:args.count], start=1):
        prompt = tokenizer.apply_chat_template(
            build_messages(question), tokenize=False,
            add_generation_prompt=True, enable_thinking=False,
        )
        batch = tokenizer(prompt, return_tensors="pt")
        current_seed = SEED + i
        torch.manual_seed(current_seed)
        start = time.monotonic()
        with torch.inference_mode():
            result = model.generate(
                **batch,
                **GENERATION,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
            )
        elapsed = round(time.monotonic() - start, 3)
        ids = result[0][batch.input_ids.shape[-1]:]
        generated = int(ids.numel())
        # Preserve the model's raw text; no repair, rewriting or "good answer" substitution.
        answer = tokenizer.decode(ids, skip_special_tokens=True).strip()
        ended_by_eos = bool(generated and int(ids[-1]) == tokenizer.eos_token_id)
        outputs.append({
            "index": i,
            "baseline_prompt_unchanged": i <= 5,
            "prompt": question,
            "raw_model_response": answer,
            "generated_token_count": generated,
            "elapsed_seconds": elapsed,
            "seed": current_seed,
            "stop_reason": "EOS" if ended_by_eos else (
                "MAX_NEW_TOKENS" if generated >= MAX_NEW_TOKENS else "OTHER"
            ),
            "observable_diagnostics_not_quality_score": observable_only(answer),
        })
    report = {
        "schema": SCHEMA,
        "profile": PROFILE,
        "reference_baseline_run": "38685295846",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "model": "Qwen/Qwen3-0.6B",
        "model_revision": "c1899de289a04d12100db370d81485cdf75e47ca",
        "verified_model_files_sha256": EXPECTED_SHA256,
        "prompt_contract": "first_5_baseline_prompts_unchanged; last_5_generic_synthetic",
        "system_message": SYSTEM,
        "example_messages": list(EXAMPLE),
        "thinking": False,
        "generation_parameters": dict(GENERATION),
        "requested_response_count": args.count,
        "actual_response_count": len(outputs),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "answers": outputs,
        "technical_result": "COMPLETED_WITH_RAW_OUTPUT" if len(outputs) == args.count else "INCOMPLETE",
        "semantic_quality_acceptance": "NOT_EVALUATED_REQUIRES_INDEPENDENT_HUMAN_REVIEW",
        "private_or_airgapped_environment_proven": False,
        "apex_integration": "NOT_EXECUTED",
        "windows_native_security": "NOT_EXECUTED",
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"QUALITY_V2_RAW_RESPONSES: {len(outputs)}/{args.count}")
    print("QUALITY_V2_HUMAN_REVIEW: REQUIRED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Public synthetic workflow: brief failure diagnostics, no secret bytes.
        print(f"QUALITY_V2_FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
