# Persian LLM — Public Synthetic-Only Free Runner

This repository is **PUBLIC** and for limited, synthetic, generic Qwen3-0.6B tests only. **No** organizational data, passwords, private model weights, private code, APEX/Mother sources, microphone or STT/TTS. It is NOT a private lab or physically air-gapped infrastructure. Nothing here establishes a Windows NTFS security PASS, product acceptance, or legal clearance for an organizational deployment.

## Manual workflows and permissions

1. [Manual Runner Preflight (NO MODEL)](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/preflight.yml) — completed: temporary Linux CPU/RAM/storage only.
2. [Authorized Qwen3-0.6B Acquisition ONLY (NO INFERENCE)](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen-acquisition-only.yml) — completed, run `38678468114`: seven public files retrieved from pinned immutable commit; the weight and tokenizer matched upstream SHA-256. **This is not an inference result.**
3. [Authorized 5–10 Persian Qwen Responses (CPU, Synthetic)](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/five-persian-responses.yml) — **first attempt failed before model execution** in run `38681069464` because the restricted model user could not read the Python smoke script at its workspace path. The targeted Workflow copy-to-`/tmp` repair has been committed but is still **not verified by a successful inference run**. The owner authorizes up to five *new* manual retry runs, with 5–10 generic synthetic Persian responses per run. The first prior failed run does not count toward these five; no more than workflow run numbers **2 through 6**, attempt 1, are allowed. Stop after the first fully successful and independently reviewed run. CPU-only standard free GitHub runner; no paid hardware.

All three workflows use **workflow_dispatch only** (manual Run workflow), never push triggers. Public standard `ubuntu-24.04` runners only. Do NOT select paid larger runners.

### Five-response test security boundary

- Exactly `Qwen/Qwen3-0.6B` revision `c1899de289a04d12100db370d81485cdf75e47ca` and the same seven public files as the prior acquisition.
- `scripts/stage_verified_qwen_for_five.py` compares *all seven received SHA-256 values* with the independent receipt of GitHub run `38678468114`. This receipt provides two upstream-verified SHA values and five independently recorded received-file values; it is not equivalent to seven upstream published checksums.
- Python CPU environment: `torch==2.6.0` from the official PyTorch CPU index, `transformers==4.51.3`, `tokenizers==0.21.1`, `safetensors==0.5.3`, `huggingface-hub==0.30.2` from PyPI. CPU/no-CUDA verification, `pip check`, and the exact installed dependency versions (including transitive) are recorded.
- **Limit:** transitive Wheel SHA-256 digests and full legal provenance of every third-party package have not been independently pinned. This is a public synthetic experiment, not a distributable production environment.
- Only after staged hashes verify does the workflow attempt IPv4/IPv6 outbound firewall rules for a dedicated non-privileged inference user (without disrupting the GitHub runner agent). If it cannot use the network controls or observes successful outbound access as that user, it stops **without inference**. Firewall prerequisites are checked before downloading model weights. Library calls are also forced to `local_files_only=True`; this is an isolated *execution step*, not a physical air gap or a guaranteed private host.
- `scripts/local_qwen_fa_smoke.py` then loads the local CPU model, asks the chosen 5–10 public/synthetic Persian prompts, and writes the raw generated text, tokens, latency, and observed process memory. No organizational dataset or app data is referenced.
- Artifacts contain **only** text replies, model SHA metadata, runtime version list, and capacity receipt. **Never upload, cache, commit, or share weights.** Artifacts expire after 1 day. The model directory and virtual environment are deleted before artifact upload. Do not store API keys or sensitive inputs in GitHub.
- A successful job is evidence only of an experimental CPU-only **text** smoke test, pending independent review; not an APEX or Windows Native acceptance.

### How to start the authorized retry test

1. Open [the Five Persian Responses workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/five-persian-responses.yml).
2. Click **Run workflow**, select `main`, choose **5** to **10** for `response_count` (start with **5**), then **Run workflow** once.
3. Share only the resulting GitHub Run URL in the original project chat for independent inspection.

Do not automatically re-run on failure: report and inspect the exact reason before using the next authorized slot. The authorization covers at most five *new* manual runs in this same workflow (run numbers 2–6; no re-run of older snapshots); no additional owner approval is needed within that narrow scope, but an engineer must review any failures before retry. The current repository has no scheduled or push-triggered model execution.

### Source and evidence

`scripts/runner_preflight.py`: free-runner capacity; `scripts/qwen_acquisition_only.py`: prior acquisition; `scripts/stage_verified_qwen_for_five.py`: verified staging; `scripts/local_qwen_fa_smoke.py`: approved synthetic local inference. External model weights are never committed.

This activity is separate from the TAMIN G1-A-R8 private Windows Native security gate. That gate remains `NOT_EXECUTED`; no product merge/freeze is implied.
