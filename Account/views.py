from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import EditUserForm, SignUpForm, LoginForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
import json
import random
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.


@login_required
def profile_index(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'index.html', )


@login_required
def following(request, username):
    if request.method == "POST":
        # کاربری که می‌خواهیم پروفایلش را فالو یا آنفالو کنیم
        target_user = get_object_or_404(User, username=username)

        # جلوگیری از اینکه کاربر خودش را فالو کند
        if request.user == target_user:
            return JsonResponse({"error": "شما نمی‌توانید خودتان را دنبال کنید."}, status=400)

        # بررسی اینکه آیا ما از قبل در لیست فالوورهای این شخص هستیم یا خیر
        if request.user in target_user.followers.all():
            target_user.followers.remove(request.user)
            follow = False
        else:
            target_user.followers.add(request.user)
            follow = True

        return JsonResponse({
            "status": "ok",
            "following": follow,
            "follower_count": target_user.followers.count()
        })

    return JsonResponse({"error": "درخواست نامعتبر است."}, status=400)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return redirect('profile:profile_index')
        else:
            print(user_form.errors)

    else:
        user_form = EditUserForm(instance=request.user)

    context = {"user_form": user_form}

    return render(request, 'edit_profile.html', context)


def signup(request):
    if request.method == 'POST':
        signup_user_form = SignUpForm(request.POST)
        if signup_user_form.is_valid():
            user = signup_user_form.save(commit=False)
            user.set_password(signup_user_form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('profile:profile_index')
    else:
        signup_user_form = SignUpForm()
    return render(request, 'register/sinup.html', {'signup': signup_user_form})


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.user_cache
            password = login_form.cleaned_data.get('password')

            if user.check_password(password):
                if user.is_active:
                    login(request, user)
                    return redirect('profile:profile_index')
                else:
                    login_form.add_error(None, "این حساب از سایت بن شده است")
            else:
                login_form.add_error('password', "رمز عبور اشتباه است")

    else:
        login_form = LoginForm()

    return render(request, 'register/login.html', {'login_form': login_form})


def logedout(request):
    logout(request)
    return redirect('Music:index')


def register(request):
    show_otp = False

    if request.method == 'POST':
        register_form = ResetPasswordForm(request.POST)

        # --- مرحله اول: ارسال کد ---
        if "send_otp" in request.POST:
            if register_form.is_valid():
                input_validate = register_form.cleaned_data.get("input_validate")

                subject = 'کد ارسال شده برای تغییر رمز در سانی فای'
                otp_code = "".join(random.choices("0123456789", k=5))
                from_email = 'aghalla.game@gmail.com'
                recipient_list = [input_validate]

                request.session['verification_code'] = otp_code
                request.session['reset_user_identyty'] = input_validate

                if "@" in input_validate:
                    try:
                        send_mail(subject, f"کد تایید شما: {otp_code}", from_email, recipient_list)
                        messages.success(request, "کد با موفقیت برای شما ایمیل شد.")
                        show_otp = True
                    except Exception as e:
                        messages.error(request, f"خطایی در ارسال ایمیل رخ داد: {e}")
                # else:  # COMMENTED: phone/SMS disabled per request
                #     print(f"SMS Subject: {subject}")
                #     print(f"SMS Code: {otp_code}")
                #     print(f"To: {recipient_list}")
                #     messages.success(request, "کد تایید پیامک شد .")
                #     show_otp = True

        # --- مرحله دوم: تایید کد ---
        elif "verify_otp" in request.POST:
            otp = request.POST.get("otp")
            saved_otp = request.session.get('verification_code')

            if not otp:
                register_form.add_error("otp", "لطفا کد تایید را وارد کنید")
                show_otp = True

            else:
                if otp == saved_otp:
                    messages.success(request, "کد تایید صحیح است!")
                    del request.session['verification_code']

                    request.session['otp_verified'] = True
                    return redirect('profile:password_change')

                else:
                    messages.error(request, "کد وارد شده صحیح نیست.")
                    show_otp = True

    else:
        register_form = ResetPasswordForm()

    return render(request, 'register/reset_pass.html', context={
        'form': register_form,
        'show_otp_field': show_otp
    })


def password_change(request):
    if not request.session.get('otp_verified'):
        messages.error(request, "لطفا ابتدا کد تایید را دریافت و وارد کنید.")
        return redirect('profile:register')

    user_identyty = request.session.get('reset_user_identyty')

    if "@" in user_identyty:
        user = get_object_or_404(User, email=user_identyty)
    # else:  # COMMENTED: phone disabled per request
    #     user = get_object_or_404(User, phone=user_identyty)
    else:  # phone disabled - only email supported
        messages.error(request, "فقط ایمیل پشتیبانی می‌شود")
        return redirect('profile:register')

    if request.method == 'POST':
        form_chenge = SetPasswordForm(user=user, data=request.POST)
        if form_chenge.is_valid():
            form_chenge.save()

            if 'otp_verified' in request.session: del request.session['otp_verified']
            if 'reset_user_identyty' in request.session: del request.session['reset_user_identyty']

            messages.success(request, "رمز عبور شما با موفقیت تغییر کرد. اکنون می‌توانید لاگین کنید.")

            return redirect('profile:login_user')
    else:
        form_chenge = SetPasswordForm(user=user)

    return render(request, 'register/chenge_pass.html', context={"password": form_chenge})
