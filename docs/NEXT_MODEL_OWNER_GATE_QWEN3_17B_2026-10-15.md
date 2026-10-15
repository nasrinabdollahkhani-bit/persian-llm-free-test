# MORTEZA_5 — Next Model Decision & Owner Gate (2026-10-15)

**STATUS: METADATA-ONLY PLANNING / NO NEW MODEL ACQUISITION / NO MODEL INFERENCE.**

## Verified baseline

- Real `Qwen3-0.6B` CPU smoke: [run 38685295846](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846), 5/5 generated; Persian language quality rejected.
- Real V2 sample: [run 38711873242](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38711873242), 10/10 generated, 8/8 no-model contracts passed, 7/7 previous-file SHA gate, but Persian semantic quality still rejected. **TECHNICAL PASS IS NOT A LANGUAGE PASS.**
- Three remaining owner-authorized rerun slots belong **only to the existing, approved Qwen3-0.6B test workflow**. These are NOT authorization to download or run a different model.

## Next candidate recommended — NO DOWNLOAD AUTHORIZATION YET

**Qwen/Qwen3-1.7B** (instruction-tuned conversation model, not `-Base`).
Official model files: https://huggingface.co/Qwen/Qwen3-1.7B/tree/main

- Published license: Apache-2.0. Organizational legal review is still required.
- Model architecture: Qwen3ForCausalLM. Requires two weight shards and a `model.safetensors.index.json`. Total index metadata weight size: **4,063,479,808 bytes** (~4.06 GB).
- Official Hugging Face published weight hashes (reference for future controlled, immutable-revision acquisition):
  - `model-00001-of-00002.safetensors`: `169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5`
  - `model-00002-of-00002.safetensors`: `912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9`
- Additional requisite files include `config.json`, `generation_config.json`, `tokenizer.json`, `tokenizer_config.json`, `model.safetensors.index.json`, `LICENSE` and possibly tokenizer support files. An exact mandatory allowlist must be checked before creating an acquisition workflow.
- Pin one **immutable full upstream commit SHA**, cross-check files and official hashes at that same revision, and verify all downloaded file hashes against the exact pinned-revision record; never use an unconstrained `main` for executable acquisition.

**Why not move directly to Qwen3-4B?** The official weight collection is ~8.06 GB and a standard public GitHub-hosted runner is listed with 4 CPU and 16 GB RAM. Float32 inference and temporary loading can exhaust RAM/ephemeral storage. A 4B trial should be preceded by a memory/disk and runtime-fit decision. The older `Qwen2.5-3B-Instruct` official model card shows a `qwen-research` license rather than Apache-2.0, and is not the preferred first next step pending a more detailed legal gate.

## Four strict gates before any new test

1. **Capacity and provenance, planning-only:** publicly verify pinned commit SHA, per-shard SHA-256, expected disk and peak RAM, approved exact files, upstream licensing and the current public standard runner spec. No weights, downloads, Python model packages, new pay-as-you-go services or organizational data.
2. **NEW owner-signed acquisition authorization** naming model `Qwen/Qwen3-1.7B`, exact revision, public hosted runner, permitted exact files, hashing, no model inference or publishing weights, no fee. Preparing a document does not grant this authorization.
3. **Separate owner-signed inference authorization** if and only if acquisition hashes match and capacity/runtime gates pass. Use an isolated synthetic CPU test with offline-only local model calls and strict no-upload rule for model weights.
4. **Independent language evaluation:** ten reproducible synthetic Persian questions, including the original five comparability questions; score 0–2 on fluency, relevance, accuracy/caution, usefulness. A successful Workflow alone never means quality/product acceptance. Do not connect APEX or real TAMIN data.

## No-cost and infrastructure conditions

GitHub docs currently list standard `ubuntu-24.04` public runners as 4 vCPU and 16 GB RAM, free and unlimited on public repositories, but storage is separately documented as 14 GB and runner specifications can change. **Recheck actual disk/RAM before acquisition**. No premium/large runner, GPU, purchase or local laptop install is approved. A public Runner is **not** an independent private or air-gapped lab, and it cannot prove Windows Native security.

## Owner's next decision — acquisition ONLY

After metadata/technical planning verification, request a narrow, separate authorization for the *download and SHA validation only* of the chosen `Qwen3-1.7B` revision. **Never infer acquisition/inference approval from the old Qwen3-0.6B repeat authorization.**

Until that new authorization: `NEXT_MODEL_DOWNLOAD=NOT_AUTHORIZED`; `NEXT_MODEL_INFERENCE=NOT_AUTHORIZED`; `APEX_INTEGRATION=NOT_AUTHORIZED`; `PRODUCT_FREEZE=NOT_AUTHORIZED`.
