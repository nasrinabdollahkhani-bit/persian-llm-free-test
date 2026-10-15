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

### Next stage — acquisition complete; inference NOT authorized

The [one-shot Qwen3-1.7B acquisition](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38734778931) completed successfully on 2026-10-15. The [independent receipt audit](docs/QWEN3_17B_ONE_SHOT_ACQUISITION_RUN_38734778931_AUDIT_FA.md) verified ZIP SHA, CRC, 11 allowlisted files, two published weight-shard digests and the tokenizer digest, and 16/16 receipt checks. GitHub log shows 35/35 pre-download tests and normal temp cleanup. Do **not** re-run this one-time acquisition workflow.

Qwen3-1.7B has **never been loaded or used for Persian inference**. Its files were deleted from the ephemeral runner, so a future inference run will need to obtain those same publicly pinned files again under a separate explicit personal-project approval. Do not request paper signatures or institutional authorization for this personal synthetic experiment. Nothing here is an APEX product acceptance.

### Current gate — explicit owner approval granted for ONE download, not inference

On **2026-10-15**, the personal-project owner said **«اجازه دانلود می‌دهم»**, in response to the narrowly specified request for one public GitHub Actions free CPU acquisition of exactly 11 pinned Qwen3-1.7B files, SHA-256 validation, temporary cleanup and a public SHA-only receipt. **This is not permission to execute the model or publish weights.** Paper-signature/organizational approval is unnecessary for this personal and entirely public/synthetic trial.

- [Owner-authorized ONE-SHOT download Workflow](.github/workflows/qwen3-17b-one-shot-acquisition.yml) — **manual dispatch only**, only run **#1** attempt **#1**, actor/repo/branch and job guarded in both YAML and Python.
- [Active one-shot acquisition wrapper](scripts/qwen3_17b_acquisition_ONE_SHOT.py) — reuses the pinned 11-file SHA checking routine from the still-locked previous candidate, calls temporary cleanup, reports only hashes.
- [14 no-network one-shot tests](scripts/test_qwen3_17b_one_shot.py), 11 metadata tests and 10 previous locked-script tests are scheduled **BEFORE downloads**. Count: 35 tests, not claimed CI-PASS until the first actual run.
- Existing [locked acquisition baseline](scripts/qwen3_17b_acquisition_PREPARED_LOCKED.py) and [inert workflow template](.github/prepared_workflows/qwen3-17b-acquisition-LOCKED.template.yml) remain inactive for historical comparison.
- The only Artifact paths are small **JSON SHA receipts**, never the model files, tensors, tokenizers, personal data, or inference output. Temp weights are cleaned on normal exit; GitHub's ephemeral runner terminates after the job. No paid runner, no installs, no GPUs, no organization data.

**Only user action pending:** open [the one-shot manual workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-one-shot-acquisition.yml), select `main`, press **Run workflow ONCE**, and share its run URL. Do not retry even if it fails; investigate the failure and request new scope/approval before another attempt.

After the actual 11-file acquisition is independently confirmed, the owner may separately approve one **synthetic Persian quality inference experiment**. Until then: Qwen3-1.7B `INFERENCE_NOT_AUTHORIZED`, `APEX_NO_INTEGRATION`, `PRODUCTION_NO_ACCEPTANCE`.
