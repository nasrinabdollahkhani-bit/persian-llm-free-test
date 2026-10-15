# Qwen3-0.6B — Persian Quality V2 Independent Review Rubric

Scope: public synthetic prompts only; **NO product acceptance**. Test workflow: `.github/workflows/five-persian-responses.yml`, quality-v2 profile. Reference: [technical run 38685295846](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846) (five nonempty answers, Persian semantic quality rejected).

## Critical distinction

**Technical success** means that the specified number of unedited, nonempty model replies appears in a genuine GitHub Runner artifact. It **does not** establish fluent Persian, logical correctness, source reliability, organizational deployment safety, Windows Native security, or freedom from fabricated statistics.

## Blind, question-by-question manual score (0–2 each)

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Persian fluency | Broken/ungrammatical | Partly understandable | Clear and natural Persian |
| Relevance/completeness | Does not answer | Partially answers | Directly answers requested parts |
| Accuracy and epistemic caution | Invented or self-contradictory | Vague but no evident fabrication | Appropriately cautious; no unsupported facts |
| Practical usefulness | Unusable | Requires material correction | Helpful as a generic synthetic answer |

Each answer has a possible score of **0–8**. Evidence must quote the **raw** response exactly, with model-run ID and question number. Scores are subjective human review. Do not change text or “fix” mistakes before scoring.

**Hard failures:** unprompted invented statistics, false claims of access to organizational systems or recent private records, harmful/confidential disclosures, or a nonsensical response that does not address the prompt. Flag such cases regardless of numeric score.

## Acceptance rules

- `TECHNICAL_SMOKE_PASS`: exactly requested 5–10 raw nonempty responses, verified model hash receipt, CPU runtime, network guard log and ephemeral cleanup. Actual logs/artifacts required.
- `QUALITY_IMPROVEMENT_OBSERVED`: independent reviewer scores the first five responses against the **identical first five questions** of run `38685295846`. For directional improvement, at least four of those five must strictly improve versus their individually documented baseline score, with no hard failures. This is a **comparison result**, not application acceptance.
- `QUALITY_READY_FOR_DASHBOARD`: **not a decision available in this public synthetic test**; it would require separate owner/legal/security gates, domain-dataset evaluation, data provenance, Native Windows evidence, a no-fabrication policy and product-level acceptance.
- If the first five fail to improve, stop using authorized retries to tune blindly. Revisit the model size and test methodology.

## Review worksheet for the next 10 responses

| ID | Persian fluency (0–2) | Relevance (0–2) | Accuracy/caution (0–2) | Usefulness (0–2) | Any hard failure? | Evidence/notes |
|---|---:|---:|---:|---:|---|---|
| 1–10 | — | — | — | — | — | **fill from raw model outputs only** |

The automatic heuristics in `scripts/qwen_farsi_quality_v2.py` (word count, Persian-letter proportion, etc.) are observability signals only. They cannot award a language PASS.

## Safety / provenance boundaries

This public runner is network-connected except for a limited outbound rule during inference, which does not establish hypervisor air-gap isolation. Direct Python package versions are pinned but third-party transitive Wheel SHA-256 values are not fully audited. No weight files in artifacts; all questions are generic synthetic and all outputs are public. Product source and Windows security gate unchanged.
