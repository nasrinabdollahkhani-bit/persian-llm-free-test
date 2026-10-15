# Persian Text Quality V2 — Baseline Comparison Sheet

**Source of baseline:** verified GitHub Actions run [38685295846](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846), Qwen3-0.6B, CPU only, five synthetic prompts, original deterministic/greedy profile. This is **real model text**, not manually rewritten. **5/5 produced, Persian semantic quality NOT accepted.**

The Quality V2 candidate holds the **same first five questions**, but adds a clearer Persian system prompt, one synthetic few-shot example, non-thinking sampling, and a 160-token budget. Improvements are a hypothesis, **not a result** until a new real run is reviewed.

| # | Baseline raw response (unchanged) | Output tokens | Time, seconds | Minimum improvement criterion for V2 |
|---|---|---:|---:|---|
| 1 | سلام! | 3 | 1.055 | Introduce itself in one understandable complete Persian sentence, not a greeting alone |
| 2 | با داده های واقعی دسترسی ندارم، میتوانم از اطلاعات مربوط با این موضوع را توضیح ده. | 47 | 7.031 | State that genuine data are unavailable and recommend checking a trustworthy source; natural grammar |
| 3 | مقایسه دو استان به دسترسی به داده نهایی انجام میکند. | 29 | 4.562 | Clearly explain at least one benefit of comparing provinces *without* fabricating numbers |
| 4 | معیار کوتاه برای ارزیابی کیفیت پاسخ فارسی: **پاسخ فارسی**. | 37 | 5.550 | Name **three distinct** language-quality criteria rather than a circular single phrase |
| 5 | بهترین اقدام اینکه اقدامات را به این شکل انجام ده که از این شرکت بهترین ارتباط را ایجاد میکند. | 55 | 7.828 | Propose asking a concrete clarifying question rather than incoherent generalities |

**Baseline duration of text generation:** 26.026 seconds total. This is not model download or runtime installation time. Output count was 5/5 and fully satisfactory Persian responses were assessed as 0/5 in the initial independent review.

## Quality V2: extended questions 6–10

6. Statistics review: ask for what the report concerns, date range, definitions, authoritative source, and expected comparison.
7. Valid data vs guesswork: distinguish verifiable evidence from ungrounded estimation in coherent Persian.
8. Uncertainty: explicitly acknowledge missing evidence and request an appropriate clarification, without pretending to know facts.
9. Summarization: suggest a pragmatic short summary of key claims and supporting evidence, not fictional specifics.
10. Comparing trends: ask for comparable time windows, definitions and denominators before comparing, without inventing values.

## Review rule

For all ten answers, retain the unedited raw text from the GitHub Artifact. The [independent rubric](FA_QUALITY_V2_INDEPENDENT_REVIEW_RUBRIC.md) scores fluency, relevance, epistemic care, and practical usefulness separately (0–2 each). At least four of the first five answers must improve on their own baseline score, with no hard failures, to claim **directional quality improvement**. **A GitHub green check or ten nonempty strings is only technical evidence, never a product-quality pass.**

## Authorization / scheduling

Owner permitted a maximum of **five new manual retries** under run-number guard 2–6, with 5–10 public synthetic replies each. Run number 2 ([38685295846](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38685295846)) consumed the first of these. **Four manual slots remain.** No new run can be started by a `push` event and this comparison document does not start a workflow. Use the existing manual [Quality V2 Workflow](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/five-persian-responses.yml), choose branch `main`, `response_count=10`, dispatch once and provide the resulting run link.

Never publish personal/organizational data or model weights. Windows native security, product integration and deployment approval are separate unexecuted gates.
