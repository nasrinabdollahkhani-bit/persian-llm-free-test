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
- [Inactive corrected retry template](.github/prepared_workflows/qwen3-17b-farsi-inference-retry-r1.template.yml), [distinct pinned SHA stage](scripts/qwen3_17b_stage_verified_inference_RETRY_R1.py), and [three extra offline tests](scripts/test_qwen3_17b_farsi10_retry_r1.py) are ready **but NOT authorized or activated**. The future retry workflow will run **63 pre-download contract tests**; GitHub has not executed that new suite.
- **DO NOT CLICK RUN OR RE-RUN** on the original [FA10 one-shot workflow](.github/workflows/qwen3-17b-farsi-inference-one-shot.yml). Its first-run authorization has been consumed; its run_number/attempt guards intentionally reject another run.
- A distinct, corrected **single-use retry** requires explicit additional personal-project owner approval. Only after that can a new manual workflow with its own first-run guard be activated. The existing 0.6B workflow and its unused retry slots are unrelated.

### LATEST EVIDENCE — successful real Qwen3-1.7B Persian inference R1; no production acceptance

[Real GitHub Actions Run 38751548673](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38751548673) completed with **SUCCESS**. Independent review of the real [artifact](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38751548673) confirmed **67/67** no-network pre-download contract tests, **11/11** files SHA matched historical acquisition Run 38734778931 (3 independent published hashes, 8 previously recorded SHA), real **10/10 raw Persian responses**, egress limited by dedicated inference UID, cleanup and no model weights in artifacts. The artifact ZIP SHA-256 matched GitHub's published digest.

**[FULL Persian quality/evidence report](docs/QWEN3_17B_FA10_R1_RUN_38751548673_REAL_EVIDENCE_QUALITY_COMPARISON_FA.md)**. The new model shows clear *relative* Persian improvement over Qwen3-0.6B V2, but 7/10 responses hit the 160-token cap and several are incomplete, repetitive or linguistically defective. Avg generation latency was **54.56 sec** per response; peak process RSS **~9.97 GiB** on 4-CPU runner. **No APEX connection, confidential data, Windows Native validation or quality acceptance.**

**DO NOT DISPATCH OR RERUN either original or corrected one-shot inference workflow.** The owner-approved single run has been consumed, the model/runtime files were cleaned. No further testing or expenses are authorized. Current product gate: `RESEARCH_ONLY / PRODUCTION_NO_GO`.

### Historical R1 authorization record — RUN ALREADY COMPLETED (DO NOT DISPATCH)

On 2026-10-15 the owner of this **personal** project explicitly approved **one corrected Qwen3-1.7B FA10 run on the standard free GitHub CPU runner**, using 10 public synthetic Persian questions and the exact 11 known model SHA-256 values. The original failed workflow **MUST NOT be re-run**.

- [**NEW manual corrected R1 workflow**](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-farsi-inference-retry-r1.yml) — owner actor and main branch only; accepts only **run #1 / attempt #1**.
- [Scope of the explicit owner's retry approval and activation](docs/QWEN3_17B_FA10_RETRY_R1_OWNER_APPROVAL_AND_ACTIVATION_2026-10-15.md).
- [Corrected previous faulty fixture and new nonempty-dir regression](scripts/test_qwen3_17b_farsi10_contracts.py). Source security validation unchanged.
- [Seven specialized corrected-retry tests](scripts/test_qwen3_17b_farsi10_retry_r1.py) include mocked all-11 staging, invalid manifest, dirty model directory and SHA mismatch; no model download during those tests.
- **67 offline pre-download unit contracts scheduled**: 11 + 10 + 14 + 8 + 17 + 7. Their CI outcomes are **NOT_VERIFIED until the actual R1 run**.
- Model, prompt profile, public data-only controls, dedicated network-restricted inference UID, temporary-weight cleanup and JSON text-only artifacts remain the same.

**Historical instruction now SUPERSEDED:** The new R1 workflow was already run successfully as Run 38751548673. **Do not click Run workflow or Re-run.** No new model execution is authorized.

**Historical state superseded by the SUCCESS evidence above.** No action is required until the owner approves or declines one specifically scoped replacement run.
