# MORTEZA_5 — رضایت و آماده‌سازی اجرای جبرانی R1

**تاریخ:** 2026-10-15  
**حکم:** `RETRY_R1_OWNER_CHAT_AUTHORIZED / WORKFLOW_ACTIVE_MANUAL_ONLY / MODEL_NOT_EXECUTED`

## مبنای تصمیم

اولین اجرای آزمایش فارسی Qwen3-1.7B در [Run 38741055594](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38741055594) به دلیل خطای Fixture آزمون شماره ۱۳، **پیش از دانلود مدل** متوقف شد: ۵۸/۵۹ آزمون موفق، هیچ وزن یا پاسخی تولید نشد. [ممیزی و اصلاح](QWEN3_17B_FA10_RUN_38741055594_FAILURE_AUDIT_AND_TARGETED_FIX_FA.md).

مالک **پروژه شخصی** در همین گفتگو صریحاً اعلام کرد:

> مجوز می‌دهم یک اجرای جبرانی تازه برای آزمایش ۱۰ پاسخ فارسی Qwen3-1.7B روی GitHub Actions رایگان آماده و فعال شود. فقط داده مصنوعی، بدون اتصال به APEX، بدون هزینه، و با کنترل هش ۱۱ فایل. اجرای مجددِ Workflow قدیمی مجاز نیست.

این تأیید فقط یک اجرای جبرانی از Workflow جدید را پوشش می‌دهد. نصب در سیستم اصلی، داده واقعی، سرویس پولی، APEX و تکرار خودکار مجاز نیستند.

## دقیقاً چه چیزی فعال شده است؟

- Workflow جدید و مستقل: [qwen3-17b-farsi-inference-retry-r1.yml](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-farsi-inference-retry-r1.yml).
- `workflow_dispatch` فقط با کاربر صاحب مخزن، شاخه `main`، `run_number == 1` و `run_attempt == 1`. همین کنترل در Source اسکریپت مرحله‌بندی مستقل نیز برقرار است.
- Runner عمومی Linux `ubuntu-24.04` استاندارد و CPU-only؛ بدون هزینه برای سرویس پولی.
- مدل `Qwen/Qwen3-1.7B` در Revision ثابت `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`؛ ۱۱ فایل با هش ثابت Artifact واقعی دریافت Run `38734778931` و سه SHA رسمی منتشرشده.
- شش مجموعه آزمون **۱۱ + ۱۰ + ۱۴ + ۸ + ۱۷ + ۷ = ۶۷** مورد، **پیش از دانلود**. کد آن‌ها آماده است؛ نتیجه اجرای ۶۷ آزمون هنوز `NOT_EXECUTED` است.
- ده سؤال دقیقاً مطابق V2 مدل 0.6B؛ ذخیره پاسخ خام، زمان و توکن، بدون دستکاری خروجی. کیفیت انسانی هنوز `NOT_EVALUATED`.
- اجرای inference با UID اختصاصی و خروجی شبکه محدودشده IPv4/IPv6، جداسازی صرفاً در سطح کاربر/سیستم‌عامل و نه Airgap.
- پاک‌سازی فایل‌های وزن و Runtime در مرحله `always` و Artifact فقط شامل متن عمومی مصنوعی، رسید SHA و نسخه Runtime.

## مرزهای حکم

- اجرای قدیمی `38741055594` نباید `Re-run` شود و Workflow یک‌بارمصرف قبلی نیز نباید دوباره آغاز شود.
- **فعال‌شدن YAML به معنی اجرای واقعی نیست**؛ در زمان ثبت این دستور هنوز `RUN_R1_NOT_TRIGGERED`.
- Source محصول، Windows Native، شواهد Airgap و تأیید عملیاتی APEX خارج از دامنه‌اند.

## فقط یک اقدام لازم

صفحه [Workflow جبرانی R1](https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/workflows/qwen3-17b-farsi-inference-retry-r1.yml) را باز کن، شاخه `main` را انتخاب کن و فقط یک مرتبه `Run workflow` را بزن. لینک Run را برای ممیزی مستقل ارسال کن؛ حتی اگر شکست بخورد، دوباره شروع نکن.
