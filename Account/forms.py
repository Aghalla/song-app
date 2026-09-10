from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.db.models import Q
from django.core.exceptions import ValidationError
import re


class ChangeUserForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'phone',
            'is_staff',
            'is_active',
            'is_superuser',
            'joined_at',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("قبلا شماره تلفن استفاده شده است")

        else:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("قبلا شماره تلفن استفاده شده است")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must be a digit")

        if not phone.startswith('09'):
            raise forms.ValidationError("Phone number must be 09 digits")

        if len(phone) != 11:
            raise forms.ValidationError("Phone number must be 11 digits")

        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if self.instance.pk:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("قبلا یوزرنیم استفاده شده است")
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("قبلا یوزرنیم استفاده شده است")

        return username


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'phone',
            'is_staff',
            'is_active',
            'is_superuser',
            'joined_at',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("قبلا شماره تلفن استفاده شده است")
        else:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("قبلا شماره تلفن استفاده شده است")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must be a digit")

        if not phone.startswith('09'):
            raise forms.ValidationError("Phone number must be 09 digits")

        if len(phone) != 11:
            raise forms.ValidationError("Phone number must be 11 digits")

        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if self.instance.pk:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("قبلا یوزرنیم استفاده شده است")
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("قبلا یوزر نیم استفاده شده است")

        return username


class EditUserForm(forms.ModelForm):
    delete_profile = forms.BooleanField(required=False, label="حذف پروفایل")

    class Meta:
        model = User
        fields = [
            "profile_pic",
            "username",
            "phone",
            "email",
            "first_name",
            "last_name",
            "bio"
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["delete_profile"]:
            if user.profile_pic:
                user.profile_pic.delete(save=False)

            user.profile_pic = None

        if commit:
            user.save()

        return user

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری از قبل وجود دارد")
        return username

    def clean_phone(self):
        pohne = self.cleaned_data["phone"]
        if User.objects.exclude(id=self.instance.id).filter(phone=pohne).exists():
            raise forms.ValidationError("این شماره قبلا ثبت شده")
        return pohne

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلا ثبت شده")
        return email


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput, max_length=50)
    password2 = forms.CharField(label='تکرار رمز', widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = User
        fields = ["username", "email", "phone"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("پسورد های یکی نیستند")
        return cd["password2"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلا استفاده شده است")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("این شماره قبلا استفاده شده است")
            if phone.isdigit():
                raise forms.ValidationError("فقط باید عدد وارد کنید")
            if not phone.startswith('09'):
                raise forms.ValidationError("شماره همراه باید با 09 شروع شود")
            if len(phone) != 11:
                raise forms.ValidationError("باید عداد 11 رقم باشند")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل تکراری است")
        return email


class LoginForm(forms.Form):
    login_input = forms.CharField(
        label="نام کاربری، ایمیل یا شماره تلفن",
        widget=forms.TextInput(attrs={'placeholder': 'username, email or phone...'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'placeholder': 'password...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        login_input = cleaned_data.get('login_input')
        password = cleaned_data.get('password')

        if login_input and password:

            user = User.objects.filter(
                Q(username=login_input) |
                Q(email=login_input) |
                Q(phone=login_input)
            ).first()

            if user is None:
                raise ValidationError("کاربری با این مشخصات یافت نشد.")

            self.user_cache = user

        return cleaned_data


class ResetPasswordForm(forms.Form):
    input_validate = forms.CharField(label="ایمیل یا شماره تلفن")
    otp = forms.CharField(max_length=5, label="کد",
                          widget=forms.TextInput(attrs={"placeholder": "کد ارسال شده برای شما"}), required=False)

    def clean_input_validate(self):
        input_validate = self.cleaned_data.get('input_validate').strip()
        if "@" in input_validate:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", input_validate):
                raise ValidationError("فرمت ایمیل وارد شده معتبر نیست")

            if not User.objects.filter(email=input_validate).exists():
                raise ValidationError("کاربری با این ایمیل یافت نشد")

        elif input_validate.isdigit():

            raise ValidationError("قابلیت پیامک هنوز در دسترس نیست")
            # if len(input_validate) != 11:
            #     raise ValidationError("طول شماره موبایل صحیح نیست")
            #
            # if not input_validate.startswith("09"):
            #     raise ValidationError("شماره موبایل باید با 09 شروع شود")
            #
            # if not  User.objects.filter(phone=input_validate).exists():
            #     raise ValidationError("کاربری با این شماره تلفن پیدا نشد")

        else:
            raise ValidationError("اطلاعات داده شده اشتباه است")
        return input_validate


class new_password_form(forms.Form):
    password1 = forms.CharField(label="رمز جدید", widget=forms.PasswordInput, max_length=50)
    password2 = forms.CharField(label="تکرار رمز", widget=forms.PasswordInput, max_length=50)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise ValidationError("رمز ها یکی نیستن")

        return cd["password2"]
