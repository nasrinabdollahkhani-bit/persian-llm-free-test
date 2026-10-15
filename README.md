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
| Qwen3-1.7B one-shot acquisition SHA receipt | [38734778931](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38734778931) | **SUCCESS**, 11/11 public files acquired; 3 official SHA-256 MATCH, 8 locally computed; 35/35 no-model contract tests; weights cleaned, **NO INFERENCE** |

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

### Latest accepted evidence: Qwen3-1.7B acquisition complete

[Real GitHub one-shot acquisition 38734778931](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38734778931) completed successfully. [Independent audit](docs/QWEN3_17B_ONE_SHOT_ACQUISITION_RUN_38734778931_AUDIT_FA.md): 11/11 public files, 3 official hashes MATCH, eight prior-archive hashes recorded, 35/35 no-model tests and cleanup. **Do not rerun acquisition**.

### CURRENT — FA10 attempt #1 blocked before downloads; targeted repair prepared

The owner-approved public synthetic Qwen3-1.7B FA10 Run [38741055594](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38741055594) finished **FAILURE** on 2026-10-15. **58 of 59 pre-download tests passed; one test fixture failed, before any model files were downloaded or any inference took place.**

The test put an intentionally malformed `bad.json` inside the model directory, which must be empty. The downloader correctly rejected the nonempty directory (`UNSAFE_MODEL_DIR`), but the test incorrectly expected a later invalid-manifest error. The fixture has been fixed by placing `bad.json` in an independent sibling location, and a new regression test explicitly checks that a nonempty model directory remains blocked before network calls. **No security check was weakened.**

- [Full failure audit, 11-hash cross-check, and repair details](docs/QWEN3_17B_FA10_RUN_38741055594_FAILURE_AUDIT_AND_TARGETED_FIX_FA.md).
- The SHA-256 lock for **all 11 public model files exactly matches** the genuine earlier acquisition artifact from Run 38734778931; ZIP checksum and CRC passed independent checking.
- Focused local mock/fixture reproduction: **2/2 passed**. **Full 60-test GitHub suite NOT rerun**.
- Qwen3-1.7B has generated **zero** real Persian responses. No APEX data, private data, model weights in artifacts, payments, or Windows validation.
- **DO NOT CLICK RUN OR RE-RUN** on the original [FA10 one-shot workflow](.github/workflows/qwen3-17b-farsi-inference-one-shot.yml). Its first-run authorization has been consumed; its run_number/attempt guards intentionally reject another run.
- A distinct, corrected **single-use retry** requires explicit additional personal-project owner approval. Only after that can a new manual workflow with its own first-run guard be activated. The existing 0.6B workflow and its unused retry slots are unrelated.

**Current state:** `SOURCE_TEST_FIX_PREPARED / ZERO_MODEL_INFERENCE / SECOND_RUN_NOT_AUTHORIZED`. No action is required until the owner approves or declines one specifically scoped replacement run.
