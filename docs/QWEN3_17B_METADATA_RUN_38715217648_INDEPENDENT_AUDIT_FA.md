# MORTEZA_5 — ممیزی مستقل گیت مقدماتی Qwen3-1.7B

**تاریخ:** 2026-10-15  
**Run:** [38715217648](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38715217648)  
**Job:** `116356150185`  
**حکم:** `METADATA_CAPACITY_PROVISIONAL_PASS / NEW_MODEL_DOWNLOAD_NOT_AUTHORIZED / NEW_MODEL_INFERENCE_NOT_AUTHORIZED`

## شواهد راستی‌آزمایی‌شده

- اجرای دستی `workflow_dispatch` روی `main`، Job نتیجه `success`، SHA اجرای گیت `f03a80ecd653bad3f86fca6fd4e7880c24e6814e`.
- آزمون‌های آفلاین استاندارد Python: **11/11 PASS**؛ شامل کنترل Revision ثابت، فایل‌ها، هش‌های ثبت‌شده و رد دست‌کاری مجوز.
- لاگ: `MODEL_DOWNLOAD: NOT_EXECUTED`، `MODEL_INFERENCE: NOT_EXECUTED`، `METADATA_VERDICT: METADATA_MANIFEST_VERIFIED`، `CAPACITY_VERDICT: PROVISIONAL_CAPACITY_MINIMUMS_MET_NOT_MODEL_FIT`.
- Artifact شماره `11963000967` فقط شامل `qwen3_17b_metadata_gate_receipt.json` است. SHA-256 ZIP دریافت‌شده و ثبت GitHub: `f6b10af80e64df8ff4c1d0e3d7f34330b9390af963f3afffc30314d8de169017`، **MATCH** و آزمون سلامت ZIP **PASS**.
- مدل مشخص‌شده: `Qwen/Qwen3-1.7B` در Revision کامل `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`؛ Allowlist شامل ۱۱ فایل و سه SHA-256 مرجع **در Manifest**. هیچ دریافت واقعی و تطبیق هش با بایت‌های وزن انجام نشده است.
- مجموع اندازه فایل‌های دو Shard: `4,063,515,592` بایت؛ `index.total_size` برابر `4,063,479,808` بایت، یعنی داده‌های Tensor بدون سربار فایل.

## ظرفیت مشاهده‌شده در Runner

| شاخص | اندازه ثبت‌شده |
|---|---:|
| CPU affinity | ۴ |
| RAM کل | 16,766,414,848 بایت (~15.615 GiB) |
| RAM آزاد زمان آزمون | 15,772,839,936 بایت (~14.690 GiB) |
| دیسک موقت آزاد | 92,111,630,336 بایت (~85.786 GiB) |
| نتیجه کنترل حداقلی | `PASS` |
| تضمین جاگیری مدل در RAM و سرعت استنتاج | `NOT_PROVEN` |

## مرز حکم

این آزمایش تنها *آمادگی فراداده‌ای و حداقل ظرفیت* را نشان می‌دهد. هیچ مدل جدیدی دانلود/اجرا نشده، هیچ وابستگی جدیدی نصب نشده و این Runner عمومی گواه جداسازی Airgap یا ممیزی Windows Native نیست. `Apache-2.0` در Manifest صرفاً مجوز اعلام‌شده است؛ بررسی حقوقی سازمانی هنوز `PENDING` است.

**گیت مالک:** گواه امضاشده مستقل برای دریافت دقیق ۱۱ فایل عمومی Qwen3-1.7B در Revision ثابت و فقط با هدف دریافت و کنترل هش باید پیش از دانلود تأیید شود؛ مجوز اجرای مدل جداگانه است. توافق برای برنامه‌ریزی یا اجرای این گیت Metadata، مجوز دانلود/استنتاج را ایجاد نمی‌کند.

**گام بعدی مجاز بدون هزینه:** مرور نتیجه، بررسی رسمی مدارک مجوز و در صورت احراز آن، آماده‌سازی محدود Workflow دانلود **بدون شروع خودکار**.
