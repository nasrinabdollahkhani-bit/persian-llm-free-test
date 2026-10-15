# Public Synthetic Persian LLM Lab — MORTEZA_5 (not product approval)

This GitHub repository is **PUBLIC**. It may contain only public synthetic questions, open model references, program code, and public hash/version/response receipts. **Do not upload internal organization data, APEX/Mother source, personal data, tokens, secrets, private receipts, or model weights.** Hosted GitHub is not a private/air-gapped lab, and none of these tests count as Windows NTFS native-security evidence or organizational approval.

## Verified earlier evidence

- [Preflight](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38677772386): temporary standard Linux CPU/RAM/disk capacity PASS.
- [Qwen3-0.6B acquisition](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38678468114): seven files at revision `c1899de289a04d12100db370d81485cdf75e47ca` downloaded; two published upstream SHA-256 values MATCH; remaining five match the recorded prior acquisition SHA values, not five independently published hashes.
- [Original five-response text run](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38681069464): FAILED before inference due to Python-script read access as a restricted user; no response produced.
- [Successful five-response text run](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846): CPU-only runtime, seven-file SHA verification, restricted-user network rule, generation, and temporary cleanup PASS; **5/5 nonempty raw replies**, but independent quality review found **0/5 fully satisfactory**, so **PERSIAN QUALITY NOT ACCEPTED**.

## Quality V2 — code prepared, NO NEW RUN

The owner authorized up to **five new** manually dispatched quality/retry runs after the first failed inference attempt: workflow run numbers **2 through 6**, run attempt 1, with **5–10 public/synthetic Persian answers each**. The successful `38685295846` is slot **1/5**; at most **four** authorized slots remain, and no repeat execution should be wasted without reviewing the preceding outcome.

The [Authorized Persian Qwen Quality V2 workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/five-persian-responses.yml) is **manual only** (`workflow_dispatch`), standard `ubuntu-24.04` runner only, never push/scheduled triggers. New profile:

- [`scripts/qwen_farsi_quality_v2.py`](scripts/qwen_farsi_quality_v2.py) — ten fixed, generic synthetic Persian questions, with first five **identical to the real baseline run**; clear Persian system message, one synthetic example, `enable_thinking=False`, documented Qwen3 non-thinking sampling parameters (`do_sample=True`, `temperature=0.7`, `top_p=0.8`, `top_k=20`), 160-token ceiling per response, and fixed per-prompt random seeds.
- Raw model responses are stored **without rewriting**. Each response includes its prompt, generated tokens, elapsed time, stop reason, and transparent, superficial length/language diagnostics. The script must always mark **semantic quality as not assessed and requiring independent human review**. Nonempty text is a technical outcome, NOT language acceptance.
- [`scripts/test_qwen_farsi_quality_v2.py`](scripts/test_qwen_farsi_quality_v2.py) — eight standard-library-only contract tests (no runtime/model/download), scheduled before package installation. **Until an actual workflow run passes, these tests are only PREPARED and NOT_EXECUTED in CI**.
- The same seven public model files are re-downloaded from the immutable revision on each new ephemeral runner, with SHA-256 cross-check against the previous public receipt. CPU dependencies remain direct-version pinned; transitive Wheel hashes are not independently proven.
- Inference runs as `qwen_infer` with fail-closed IPv4/IPv6 outbound restriction at the UID boundary. That is not proof of hypervisor isolation or a physical air gap. No APEX integration, audio, STT, TTS, Windows test or product Source mutation.
- Only the tiny **public synthetic JSON text report**, environment version list, capacity report and SHA metadata are allowed in a 1-day Artifact. No weights or model runtime uploaded. Temporary bytes are removed at the end.

Independent score rules: [Persian Quality V2 review rubric](docs/FA_QUALITY_V2_INDEPENDENT_REVIEW_RUBRIC.md). Human evaluators compare the first five identical questions against the raw baseline; technical 10/10 is **not** a quality PASS.

### Single next step, only after reviewing the prepared code

Open [the manual quality-v2 Workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/five-persian-responses.yml), click **Run workflow**, choose **main**, set **response_count = 10**, and manually trigger **once**. Share its run URL for independent quality evaluation of all ten raw answers. If any step fails, stop and inspect before further retries. A successful GitHub Job alone does not mean the answers are suitable for use in the dashboard.

**No purchases, paid GPU, private organizational datasets, auto-trigger, production integration or independent Windows Native execution.**


## Next candidate: Qwen3-1.7B — metadata gate ONLY (NO DOWNLOAD)

Owner agreed to **plan** the next larger model candidate after Qwen3-0.6B achieved 10/10 technical outputs but failed Persian semantic quality. This agreement is **not** an independently authenticated, signed acquisition or inference authorization.

- Fixed upstream revision: `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`; official model branch remains separate from this fixed immutable revision.
- The [11-file manifest](metadata/qwen3_17b_pinned_manifest.json) records two weight-shard SHA-256 values, tokenizer SHA-256, exact known weights file sizes, and the distinction between index tensor bytes and physical shard bytes.
- [Metadata-only runner workflow](.github/workflows/qwen3-17b-metadata-only.yml) is **manual dispatch only**, on a standard `ubuntu-24.04` public runner, with eleven no-download Python stdlib tests and CPU/RAM/disk capacity evidence. **Never downloads model weights or installs inference packages.**
- [Acquisition signature template in Persian](docs/QWEN3_17B_NEW_OWNER_ACQUISITION_AUTHORIZATION_TEMPLATE_FA.md) documents the separate signed-owner gate. **Do not put names/signatures/identity documents in this public repo.**
- Both Qwen3-1.7B model acquisition and inference remain **NOT_AUTHORIZED**. Even a passed metadata gate cannot approve model runtime, Windows security, paid infrastructure, actual private/Airgap isolation or APEX integration.
