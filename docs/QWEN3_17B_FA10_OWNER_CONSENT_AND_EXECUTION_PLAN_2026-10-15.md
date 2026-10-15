# MORTEZA_5 — Qwen3-1.7B / آزمایش ده پاسخ فارسی

**تاریخ:** 2026-10-15  
**وضعیت:** `PERSONAL_OWNER_CHAT_APPROVED_ONE_RUN / PREPARED / NOT_EXECUTED`

## محدوده موافقت

پس از نتیجه موفق دریافت مدل در [Run 38734778931](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38734778931)، مالک پروژه شخصی به سؤال مشخص درباره **یک بار اجرای Qwen3-1.7B با ۱۰ سؤال فارسی مصنوعی روی GitHub Actions رایگان** پاسخ «بله» داد. این موافقت شامل دریافت دوباره همان ۱۱ فایل عمومی برای اجرای مدل، کنترل هش‌ها و انتشار فقط پاسخ‌های مصنوعی است؛ نه داده خصوصی، سرور پولی یا اتصال به APEX.

## فایل‌های آماده

- [Workflow یک‌بارمصرف FA10](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-farsi-inference-one-shot.yml)
- [اسکریپت مرحله‌بندی با ۱۱ SHA](../scripts/qwen3_17b_stage_verified_inference.py)
- [اسکریپت اجرای ده پاسخ](../scripts/qwen3_17b_farsi10_inference.py)
- [هش‌های منجمد دریافت قبلی](../metadata/qwen3_17b_prior_acquisition_11_sha_lock.json)
- [۱۶ آزمون جدید بدون مدل](../scripts/test_qwen3_17b_farsi10_contracts.py)

نسخه ثابت مدل: `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`.

سؤالات و تنظیمات تولید عین آزمون Qwen3-0.6B V2 هستند. خروجی، متن خام، زمان، تعداد توکن، نسخه‌های runtime و گزارش SHA خواهد بود. مرور مستقل کیفیت فارسی پس از دریافت نتیجه ضروری است. هیچ قبولی کیفیت یا اجرای مدل در این مرحله ادعا نمی‌شود.

**بازبینی ایستای فایل‌های جدید: ۲۱/۲۱ PASS.** پنج بسته آزمون Python جمعاً ۵۹ مورد، برای اجرا پیش از دانلود در Workflow برنامه‌ریزی شده‌اند، اما هنوز در GitHub اجرا نشده‌اند.

**اقدام بعدی:** صفحه Workflow را باز کن؛ شاخه `main`، دکمه `Run workflow` را فقط یک بار بزن و لینک Run را بفرست. اجرای دوباره نیاز به بررسی نتیجه و مجوز جدید دارد.

این آزمایش شخصی، گواه تأیید محصول، Airgap یا Windows Native نیست.
