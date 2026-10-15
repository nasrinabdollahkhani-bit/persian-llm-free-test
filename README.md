# Persian LLM Free Test — Public Synthetic-Only Lab

This public repository uses **standard free GitHub-hosted runners** for limited, generic experiments. It is **not** a private lab, a physically air-gapped system, an APEX/Mother integration, a Windows NTFS security test, or a production acceptance gate. All logs and small receipts may be public. Never add organizational data, proprietary source, secrets, sensitive prompts or private receipts.

## Current workflows — manually dispatched only

**1. Manual Runner Preflight (NO MODEL)** — `.github/workflows/preflight.yml`

Measures CPU/RAM/disk capacity only. Previously completed successfully. It does not download models or packages and cannot establish a private lab.

**2. Authorized Qwen3-0.6B Acquisition ONLY (NO INFERENCE)** — `.github/workflows/qwen-acquisition-only.yml`

The owner provided a narrow acquisition authorization for this public repository:
- exactly seven **public** files in `Qwen/Qwen3-0.6B` pinned at `c1899de289a04d12100db370d81485cdf75e47ca`;
- files: `LICENSE`, `README.md`, `config.json`, `generation_config.json`, `tokenizer_config.json`, `tokenizer.json`, `model.safetensors`;
- temporary standard Linux runner, **no extra paid infrastructure**, no Python package installation, no model loading/inference, no other assets, no product data;
- cross-check received SHA-256 and byte size against upstream-published expected values for `model.safetensors` and `tokenizer.json`;
- calculate SHA-256 of the other five files obtained at the fixed commit, while marking these as **not independently upstream-SHA-pinned**;
- store downloaded bytes **only in an ephemeral temporary directory**, removed at job exit; **never** upload or cache the weights;
- publish only `qwen_acquisition_receipt.json`, a small public metadata-only hash/size receipt with 1-day retention.

This workflow uses only `workflow_dispatch` (no `push` or scheduled trigger) and checks repository, actor and default branch before running. **Creating this file does not start acquisition.**

### How to invoke the authorized acquisition stage

Visit [the manual acquisition workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen-acquisition-only.yml), click **Run workflow**, choose `main`, and click **Run workflow**. Afterwards share only the Run link. Failed or blocked downloads must remain FAIL/BLOCKED; do not claim that receipt hashes were verified until checking real run output.

The success criterion is `SHA_VERIFIED_TWO_UPSTREAM_AND_SEVEN_RECEIVED`. No model execution is done or authorized by this workflow.

### Boundaries

The separate `scripts/local_qwen_fa_smoke.py` is an **untriggered preparation example only**. Running it or adding an inference workflow requires a new, independent explicit authorization. Model and Python runtime execution **remain NOT_AUTHORIZED**. A public runner is not a substitute for authorized independent Windows Native security evidence, and cannot establish organizational deployment readiness.

The hosted runner may fail if upstream transfers are unavailable or GitHub changes free-runner resource limits; failed outcomes should be reported as-is. Public standard runners are documented by GitHub as no-charge for public repositories; do not select larger runners or paid storage/features.
