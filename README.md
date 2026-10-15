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

### CURRENT: owner-approved one-time Persian FA10 experiment — CODE PREPARED, NO MODEL RUN YET

On 2026-10-15 the personal-project owner responded **«بله»** to the explicit request to run **Qwen3-1.7B once for ten synthetic Persian responses on a free CPU GitHub Actions runner**. This authorizes the required re-download and hash verification of the same 11 public files **in the single inference run**. It does not authorize TAMIN/APEX access, private data, paid resources, or additional runs.

- [Prepared manual **one-shot FA10 workflow**](.github/workflows/qwen3-17b-farsi-inference-one-shot.yml) — only run #1 attempt #1; public `main` branch, repo-owner actor, standard free `ubuntu-24.04`.
- [Execution and consent record](docs/QWEN3_17B_FA10_OWNER_CONSENT_AND_EXECUTION_PLAN_2026-10-15.md).
- [Frozen 11-file digest lock](metadata/qwen3_17b_prior_acquisition_11_sha_lock.json), based on accepted run 38734778931. The model is loaded ONLY after all eleven files have been checked.
- [Ten-response script](scripts/qwen3_17b_farsi10_inference.py) uses identical 10 public synthetic prompts, few-shot/system and generation settings from the completed Qwen3-0.6B V2 run 38711873242; it publishes raw, unedited text, token count, latency and stop reason for independent Persian semantic scoring.
- **59 pre-download unit tests** have been authored/scheduled (11 metadata, 10 locked baseline, 14 one-shot acquisition, 8 V2 prompt, 16 new 1.7B contracts). Do not claim CI-PASS until the new workflow actually runs.
- Source/static review: **21/21 checks PASS**. This is not equivalent to runtime, dependency supply chain, or Windows native validation.
- CPU inference uses a dedicated non-root user with outgoing IPv4/IPv6 blocked, and offline-only model loading; no proof of genuine enterprise air-gap.
- Models, pip runtime and temporary user outputs are cleaned after the run; only short SHA metadata, public synthetic raw answers and runtime versions may be uploaded.

**Only required owner action now:** open [the FA10 one-shot Workflow page](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-farsi-inference-one-shot.yml), select `main`, and click **Run workflow once**. Send its run URL here for independent checking and honest Persian-quality comparison. Avoid retrying until the first result is reviewed.

No Qwen3-1.7B inference has yet happened; no APEX integration, Windows/NTFS certification, private TAMIN data or deployment acceptance.
