# MORTEZA_5 — ممیزی مستقل شکست اولین آزمون FA10 و اصلاح هدفمند

**تاریخ:** 2026-10-15  
**Run:** https://github.com/nasrinabdollahkhani-bit/persian-llm-free-test/actions/runs/38741055594  
**Job:** `116442559813`  
**حکم:** `PRE-DOWNLOAD_TEST_FAILURE / NO_MODEL_ACQUIRED / ZERO_INFERENCE / ONE_SHOT_CONSUMED`

## واقعیت اجرای GitHub

- اجرای دستی اول، تلاش اول، نتیجه نهایی `failure`، روی `main` در SHA `b21608d71ac9ad5c584c293f6b2174597f0ca8a4`.
- چهار گروه آزمون: **11/11، 10/10، 14/14 و 8/8 PASS**.
- گروه پنجم: **15/16 PASS، یک ERROR**؛ مجموع **58 موفق از 59 آزمون**.
- خطای دقیق: `test_13_manifest_checked_before_any_download`، خط ۱۰۳ از `scripts/test_qwen3_17b_farsi10_contracts.py`.
- آزمون برای آزمایش Manifest نامعتبر `bad.json` را داخل همان پوشه مدل قرار داده بود. نگهبان امنیتی `stage()` درست و به‌موقع `RuntimeError("UNSAFE_MODEL_DIR")` صادر کرد، چون پوشه مدل باید کاملاً خالی باشد. آزمون به‌غلط انتظار `ValueError/KeyError` از Manifest داشت؛ منبع شکست fixture آزمون است، **نه ثابت‌شدن نقص مدل**.
- مراحل نصب Runtime، دریافت مجدد ۱۱ فایل و تولید ۱۰ پاسخ **همگی SKIPPED** شدند.
- مرحله Cleanup اجرا و `NO_MODEL_WEIGHTS_IN_REPOSITORY_WORKSPACE` ثبت شد.
- **هیچ Artifact و هیچ پاسخ فارسی منتشر نشد**.

## اصلاح انجام‌شده؛ بدون تضعیف امنیت

در فایل `scripts/test_qwen3_17b_farsi10_contracts.py`:

1. آزمون شماره ۱۳ اکنون `bad.json` را در **پوشه والدِ مستقل** و نه در ریشه مدل می‌نویسد؛ پوشه `empty_model` واقعاً خالی می‌ماند تا کنترل Manifest نامعتبر فراخوانی شود.
2. آزمون مستقل `test_13b_nonempty_model_dir_fails_closed_before_download` اضافه شد که وجود هر فایل ناخواسته در پوشه مدل را باعث `UNSAFE_MODEL_DIR` می‌داند و تأیید می‌کند هیچ تابع دانلود فراخوانی نشده است.
3. Source امنیتی `stage()` و کد inference برای این اصلاح **تغییر نکردند**.
4. بررسی هدفمند محلیِ رفتار دو Fixture با داده Mock و بدون شبکه: **2/2 PASS**. این اجرای هدفمند، جایگزین آزمون کامل ۶۰ مورد روی GitHub Runner نیست.

**Candidate فعلی: 11 + 10 + 14 + 8 + 17 = 60 تست تعریف‌شده.** این ۶۰ تست هنوز در GitHub به‌صورت کامل دوباره اجرا نشده‌اند.

## کنترل مستقل قفل SHAها

Artifact اصلی دریافت عمومی مدل از Run موفق `38734778931` دوباره دانلود و با فایل Lock جدید تطبیق داده شد:

- Artifact ID `11972435891` و SHA-256 ZIP `a8e6b3e88a41dcb8087602d8b0f9a8214d4a9ec2e363a43aa8c4ca8731034d91`.
- ZIP CRC: **PASS**.
- یازده نام فایل: **EXACT MATCH**.
- یازده SHA-256: **11/11 MATCH** با `metadata/qwen3_17b_prior_acquisition_11_sha_lock.json`.
- سه SHA مرجع منتشرشده و هشت SHA محاسبه‌شده از اجرای قبلی، از هم متمایزند.

## وضعیت مجوز و ادامه

مجوز قبلی مالک پروژه شخصی برای **یک اجرای FA10** بود. اجرای `38741055594` اولین Run بود و مجوز اجرای اضافی از آن برداشت نمی‌شود. محافظ `run_number == 1` و `run_attempt == 1` در Workflow قبلی فعال است؛ کلیک مجدد روی همان Workflow یا Rerun صحیح نیست.

**گیت بعدی:** تنها در صورت رضایت صریح مالک برای **یک اجرای جبرانی تازه**، نسخه مجزا با Workflow یک‌بارمصرف جدید آماده/فعال شود؛ قبل از دریافت مدل، تمام ۶۰ تست اجرا شوند و در صورت خطا همان‌جا Fail-Closed شود. هیچ داده سازمانی، APEX، Runner پولی یا انتشار وزن مجاز نیست. تنها پس از تولید پاسخ خام می‌توان کیفیت فارسی Qwen3-1.7B را ارزیابی کرد.

**Status:** `TARGETED TEST_FIX_COMMITTED / PRIOR_HASHES_11_OF_11_VERIFIED / NO_RETRY_EXECUTED`.
