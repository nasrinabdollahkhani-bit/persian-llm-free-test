# Public Synthetic Persian LLM Test — MORTEZA_5

**PUBLIC REPOSITORY. Synthetic information ONLY.** No TAMIN, APEX, Mother system, customer, personal, organizational or confidential data. No paid runners, no local-laptop installation, no model weights in GitHub source or artifacts. Not a private lab, not a hypervisor airgap and not Windows Native security evidence. No permission for deployment or product freeze.

## Observed results (real GitHub Actions evidence)

| Stage | Run | Outcome |
| --- | --- | --- |
| Runner capacity preflight | [38677772386](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38677772386) | PASS; capacity only |
| Qwen3-0.6B public acquisition + SHA | [38678468114](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38678468114) | 7/7 received; 2 upstream hashes matched; no inference |
| Initial Qwen3-0.6B text test | [38681069464](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38681069464) | FAIL before inference (restricted user could not open Python script) |
| Corrected Qwen3-0.6B text test | [38685295846](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846) | 5/5 synthetic texts generated, Persian quality rejected |
| Qwen3-0.6B V2 text-quality experiment | [38711873242](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38711873242) | 10/10 texts generated, **Persian quality rejected** |
| Qwen3-1.7B *metadata-only* preflight | [38715217648](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38715217648) | 11/11 manifest contract tests PASS, provisional capacity PASS, **NO new model downloaded or run** |

Three original approved Qwen3-0.6B retry slots remain unused. They **DO NOT transfer** to Qwen3-1.7B. Because its Persian quality was poor in two real runs, **do not waste the remaining slots**.

## Current next-model gate — 2026-10-15

The personal-project owner agreed to **planning and preparation** of `Qwen/Qwen3-1.7B`, pinned to immutable revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`.

- [Pinned public 11-file manifest](metadata/qwen3_17b_pinned_manifest.json) — two official model weight shard hashes + tokenizer hash, recorded sizes and licensing metadata.
- [Real metadata/capacity audit](docs/QWEN3_17B_METADATA_RUN_38715217648_INDEPENDENT_AUDIT_FA.md) — 4 CPU affinity, ~15.6 GiB RAM total and ~85.8 GiB temporary disk free. **This does not establish inference fit.**
- [Metadata-only active workflow](.github/workflows/qwen3-17b-metadata-only.yml) — manual only, does not download weights.
- [Prepared hard-LOCKED acquisition source](scripts/qwen3_17b_acquisition_PREPARED_LOCKED.py) — contains a full fixed-revision HTTPS/allowlist/file-size/SHA256/temp-cleanup routine, but `ACQUISITION_ENABLED = False` causes **fail-closed before network**.
- [Ten prepared no-network lock tests](scripts/test_qwen3_17b_acquisition_LOCKED.py) — code present; no model test or new download authorized. They are NOT described as CI-passed until actually run.
- [Inert workflow template](.github/prepared_workflows/qwen3-17b-acquisition-LOCKED.template.yml) — deliberately **OUTSIDE** `.github/workflows/` and cannot be selected as an active GitHub Actions workflow.
- [Personal-owner chat consent instructions](docs/QWEN3_17B_NEW_OWNER_ACQUISITION_AUTHORIZATION_TEMPLATE_FA.md) — a clear, scoped reply in this conversation is sufficient for personal public-model download approval; **no paper signature or organizational signoff is required**.

### Next actual owner gate

The personal-project owner must explicitly consent **in this chat** to exactly one public GitHub-hosted standard CPU runner job acquiring only the pinned 11 files, checking hashes, deleting all model bytes after the job, publishing only a public SHA receipt, with **NO inference** and no spending. This is **not** an organizational approval process.

Only after the owner's explicit chat approval and independent code review may a reviewed source change unlock the downloader and turn the inert template into a **manually invoked** workflow. Do not add public `workflow_dispatch` consent inputs and do not weaken the model or host guards.

**Model inference requires a second, separate explicit owner chat approval after actual acquisition checksum verification.** Neither a chat agreement to prepare nor metadata-capacity PASS is an execution license. No TAMIN/APEX connection, organizational dataset, Windows acceptance or product freeze follows.

This repository intentionally cannot automatically start the Qwen3-1.7B acquisition at its current locked state.
