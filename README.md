# Persian LLM — Free, Public, Synthetic Test

This repository is for a **generic educational smoke test of a local Persian-language model** on standard, no-charge GitHub-hosted runners. It is **not** a secure or private organizational lab, production certification, Windows NTFS verification, or evidence of a physically air-gapped system.

## Safe first step

The only enabled GitHub Actions workflow is **Manual Runner Preflight**. It:
- runs **only** when manually dispatched from the Actions tab;
- uses a standard `ubuntu-24.04` GitHub-hosted runner;
- prints Linux CPU, memory, disk and Python environment capacity;
- does **not** install packages, download a model, invoke model inference, or use organizational data;
- has a five-minute timeout and read-only repository permission.

The workflow **does not run on push**. A separate written approval and a verified dependency/model supply chain are required before any future model acquisition or execution.

A stand-alone example script, `scripts/local_text_smoke.py`, is provided solely as **unexecuted preparation**. It has no Actions trigger and accepts only a local model directory. Its existence must not be interpreted as permission to run, or as a PASS.

### Privacy boundary

This repository and its job logs/artifacts are public. **Never** upload internal source code, organizational records, real personal data, licenses/keys/secrets, private receipts, or confidential model or application artifacts.

### Expected status

`MODEL_DOWNLOAD=NOT_AUTHORIZED` / `MODEL_EXECUTION=NOT_AUTHORIZED` / `WINDOWS_NATIVE=NOT_EXECUTED`.

The preflight checks capacity only; it cannot establish offline isolation or product security.
