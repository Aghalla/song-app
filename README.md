# 🎵 Song - سیستم مدیریت موسیقی

یک پروژه جنگو برای مدیریت و پخش موسیقی با امکانات کاربری و مدیریت آلبوم‌ها.

## امکانات

- ثبت‌نام و ورود کاربران
- آپلود و مدیریت موسیقی
- پخش آنلاین موسیقی
- دسته‌بندی و جستجوی آهنگ‌ها
- رابط کاربری فارسی

## نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.12+
- PostgreSQL
- pip

### مراحل نصب

1. **کلون کردن پروژه**
```bash
git clone https://github.com/your-username/song.git
cd song
```

2. **ساخت محیط مجازی**
```bash
python -m venv .venv
# ویندوز
.venv\Scripts\activate
# لینوکس/مک
source .venv/bin/activate
```

3. **نصب وابستگی‌ها**
```bash
pip install -r requirements.txt
```

4. **ساخت فایل .env**
فایل `.env.example` رو کپی کنید و نامش رو به `.env` تغییر بدید:
```bash
cp .env.example .env
```
سپس مقادیر دیتابیس و ایمیل رو توی فایل `.env` پر کنید.

5. **اجرای مایگریشن‌ها**
```bash
python manage.py migrate
```

6. **ساخت ادمین**
```bash
python manage.py createsuperuser
```

7. **اجرای سرور**
```bash
python manage.py runserver
```

## متغیرهای محیطی

فایل `.env` رو با این مقادیر پر کنید:

| متغیر | توضیح |
|--------|-------|
| `DATABASE_ENGINE` | موتور دیتابیس (پیش‌فرض: sqlite3) |
| `DATABASE_NAME` | نام دیتابیس |
| `DATABASE_USER` | نام کاربری دیابتابیس |
| `DATABASE_PASSWORD` | رمز عبور دیتابیس |
| `DATABASE_PORT` | پورت دیتابیس |
| `EMAIL_HOST_USER` | ایمیل ارسال‌کننده |
| `EMAIL_HOST_PASSWORD` | رمز عبور ایمیل |

## ساختار پروژه

```
song/
├── Account/          # اپ مدیریت کاربران
├── Music/            # اپ مدیریت موسیقی
├── Static/           # فایل‌های استاتیک (CSS, JS)
├── Media/            # فایل‌های آپلود شده
├── templates/        # قالب‌های HTML
├── song/             # تنظیمات پروژه
└── manage.py
```

## تکنولوژی‌ها

- **جنگو** - فریمورک وب پایتون
- **PostgreSQL** - دیتابیس
- **DRF** - رابط برنامه‌نویسی کاربردی
- **Celery** - پردازش پس‌زمینه

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.
