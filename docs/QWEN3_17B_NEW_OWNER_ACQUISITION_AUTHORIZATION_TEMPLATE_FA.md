# MORTEZA_5 — الگوی مجوز مستقل دریافت Qwen3-1.7B

**این فایل فقط الگوی متن است؛ مجوز امضاشده محسوب نمی‌شود.**

**وضعیت: ACQUISITION NOT_AUTHORIZED / INFERENCE NOT_AUTHORIZED**

## مشخصات دقیق درخواست

- مدل: `Qwen/Qwen3-1.7B` (نسخه مکالمه؛ نه `-Base`)
- Revision ثابت و کامل: `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`
- فهرست مجاز: فقط ۱۱ فایل مشخص‌شده در `metadata/qwen3_17b_pinned_manifest.json`
- دو فایل وزن با SHA-256 منتشرشده:
  - `model-00001-of-00002.safetensors`: `169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5`
  - `model-00002-of-00002.safetensors`: `912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9`
- `tokenizer.json`: `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`
- حجم فایل‌های وزن (با Header): **۴٬۰۶۳٬۵۱۵٬۵۹۲ بایت**. مقدار `index.total_size`، **۴٬۰۶۳٬۴۷۹٬۸۰۸ بایت**، صرفاً حجم داده‌های Tensor است.
- محیط: فقط GitHub Actions عمومی `nasrinabdollahkhani-bit/persian-llm-free-test`، Runner استاندارد Linux x64، CPU، بدون GPU پولی، بدون داده سازمانی، بدون تغییر Source محصول یا APEX.
- محدوده درخواست احتمالی مالک: **فقط یک نوبت دریافت عمومی و راستی‌آزمایی هش روی Runner موقت**، عدم انتشار وزن‌ها، عدم حفظ وزن‌ها در Artifact، ثبت رسید غیرحساس و حذف بایت‌ها در پایان.
- دانلود وابستگی Runtime، بارگذاری یا اجرای مدل، استنتاج، انتشار پاسخ و استفاده عملیاتی **ممنوع است**؛ برای اجرای مدل مجوز جداگانه لازم خواهد بود.

## متن پیشنهادی برای تصمیم رسمی مالک

«اینجانب در جایگاه مالک/نماینده مجاز، صرفاً **یک نوبت دریافت موقت ۱۱ فایل عمومی Qwen3-1.7B** با Revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` و کنترل SHA-256، فقط در Runner استاندارد رایگان GitHub مخزن عمومی مشخص‌شده، بدون انتشار وزن‌ها یا داده خصوصی و بدون اجرای مدل، را تأیید / رد می‌کنم. این تصمیم هیچ مجوزی برای استنتاج، نصب بر دستگاه اصلی، اتصال به APEX یا عبور از گیت امنیتی مستقل ایجاد نمی‌کند.»

**مدارک احراز مالکیت، تاریخ، امضا یا تأیید سازمانی باید از مسیر خصوصی و مجاز ارائه شوند. به مخزن عمومی GitHub بارگذاری نشوند.** صرف تأیید چتی یا وجود این فایل، گیت امضای مالک را نمی‌بندد.

## وضعیت گیت

- فهرست و Revision: **PREPARED**
- SHA-256 رسمی دو Shard و Tokenizer: **DOCUMENTED, NOT_DOWNLOADED**
- گیت حداقل ظرفیت: **CODE_PREPARED, NATIVE_RUNNER_NOT_EXECUTED**
- بررسی حقوقی مجوز Apache-2.0: **PENDING**
- دریافت وزن‌ها: **NOT_EXECUTED**
- اجرای مدل: **NOT_EXECUTED**
- هرگونه ادعای کیفیت فارسی: **NOT_EVALUATED**

لینک Workflow صرفاً ظرفیت/Manifest، بدون دریافت مدل:
https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-metadata-only.yml
