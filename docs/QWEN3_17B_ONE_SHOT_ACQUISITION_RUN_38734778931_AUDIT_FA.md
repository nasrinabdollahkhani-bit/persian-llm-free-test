# MORTEZA_5 — ممیزی دریافت یک‌باره Qwen3-1.7B / Run 38734778931

**تاریخ:** 2026-10-15  
**Run:** https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38734778931  
**Job ID:** `116421205524`  
**Artifact ID:** `11972435891`  
**Head commit:** `01ffbfd340430aa9fb2f60944cedb2810dcb3b07`  
**حکم محدود:** `ACQUISITION_SHA_RECEIPT_ACCEPTED / NO_INFERENCE / NO_APEX`

## شواهد مستقلاً خوانده‌شده

- GitHub Action: `completed/success`، اجرای دستی روی `main`، `run_number=1`، `run_attempt=1`، actor برابر صاحب مخزن.
- سه بسته آزمایش استاندارد Python، هر کدام PASS: **11 + 10 + 14 = 35/35** (پیش از دانلود). این‌ها آزمون‌های کنترل و Mock هستند، نه اجرای مدل.
- مرحله دانلود GitHub: `FILES_PROCESSED: 11`، `MODEL_INFERENCE: NOT_EXECUTED`، `TEMPORARY_WEIGHTS: DELETED_ON_NORMAL_EXIT`، `REASON_CODE: NONE`.
- کنترل محیط کار: `NO_MODEL_BYTES_IN_WORKSPACE`.
- ZIP شواهد از GitHub دریافت و باز شد؛ SHA-256 واقعی ZIP **`a8e6b3e88a41dcb8087602d8b0f9a8214d4a9ec2e363a43aa8c4ca8731034d91`** برابر مقدار ثبت‌شده GitHub است. آزمون CRC آرشیو **PASS**. داخل ZIP **فقط دو JSON** است؛ هیچ فایل وزن منتشر نشده است.
- فایل `qwen3_17b_acquisition_sha_only_receipt.json` دارای ۱۱ نام یکتا و دقیقاً منطبق با Allowlist است. اندازه همه فایل‌ها مجموعاً **4,079,448,540 bytes**؛ اندازه دو Shard وزن مجموعاً **4,063,515,592 bytes**.
- ۱۶ کنترل مستقل روی SHA آرشیو، CRC، ترکیب فایل‌ها، Allowlist، Rev، اندازه وزن، ۳ هش رسمی، هشت هش صرفاً محاسبه‌شده، محدوده اجرای بدون inference، رسید پاک‌سازی و ظرفیت: **16/16 PASS**.
- ظرفیت مشاهده‌شده در رسید جدید: چهار هسته در affinity، RAM کل حدود 15.61 GiB و دیسک موقت آزاد حدود 85.79 GiB. **جاگیری واقعی مدل در حافظه هنوز تأیید نشده است.**

## تطبیق منتشرشده SHA-256

| فایل | SHA-256 ثبت‌شده از بایت‌های واقعی | حکم |
|---|---|---|
| `model-00001-of-00002.safetensors` | `169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5` | MATCH منتشرشده |
| `model-00002-of-00002.safetensors` | `912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9` | MATCH منتشرشده |
| `tokenizer.json` | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` | MATCH منتشرشده |

هشت فایل دیگر `LICENSE`, `README.md`, `config.json`, `generation_config.json`, `merges.txt`, `model.safetensors.index.json`, `tokenizer_config.json` و `vocab.json` SHA-256 محاسبه‌شده دارند؛ **برای این هشت مورد تطبیق مستقل با هش منتشرشده ادعا نمی‌شود.**

## مرز یافته‌ها و ریسک‌های باقیمانده

1. دریافت مدل اثبات‌شده، **معادل اجرای موفق مدل نیست**. وزن‌ها طبق لاگ پاک و Runner پایان یافته است. برای اجرای آینده روی Runner تازه، دریافت دوباره وزن‌ها لازم خواهد بود؛ این نیاز به رضایت جداگانه کاربر برای *اجرای مدل و دریافت مقتضی آن* دارد.
2. فایل `qwen3_17b_metadata_gate_receipt.json` مربوط به *مرحله مستقل پیش‌بررسی* است و حاوی `model_download=NOT_EXECUTED` و فیلد قدیمی `acquisition_owner_signed_authorization=NOT_PROVIDED_OR_VERIFIED` است؛ این‌ها در مورد همان مرحله پیش‌بررسی صحیح‌اند، اما **حکم مرحله دانلود اصلی نیستند**. رضایت شخصی کاربر برای همین اجرای دانلود در گفتگو ثبت شده بود؛ امضای سازمانی مطالبه نمی‌شود.
3. حذف فایل‌های موقت بر اساس خروج عادی برنامه و لاگ Runner گزارش شده است؛ بررسی دیسک خام Runner پس از پایان به‌صورت مستقل ممکن نیست. شواهد ZIP و Workspace حاوی وزن نیستند.
4. این GitHub عمومی، Airgap سازمانی، ممیزی Windows Native یا تأیید امنیتی APEX نیست. هیچ داده خصوصی، مدل اجرایی، STT/TTS یا اتصال داشبورد جزو این کار نبوده است.
5. Workflow یک‌بارمصرف **دیگر نباید اجرا یا rerun شود**. `run_number=2` یا `run_attempt=2` در قراردادهای Job و Python رد می‌شوند.

## مرحله بعد — فقط پس از رضایت مستقل شخصی مالک

یک آزمایش محدود **۱۰ پاسخ فارسی Synthetic** با مدل `Qwen/Qwen3-1.7B` و همان Revision ثابت، تنها روی Runner رایگان CPU؛ پنج سؤال نخست دقیقاً مشابه مبنای Qwen3-0.6B، پنج سؤال بعدی Synthetic، ثبت Raw response/زمان/توکن/علت توقف، بدون استفاده از اطلاعات TAMIN یا اتصال APEX. قبل از اجرا باید تناسب CPU/RAM و حدود زمان بررسی شود. پس از اجرا، مقایسه مستقل کیفیت فارسی، نه ادعای قبولی از روی ۱۰/۱۰ خروجی.

**مدل جدید هنوز اجرا نشده است و مجوز دانلود قبلی صرفاً مربوط به دریافت/کنترل هش بوده است.**
