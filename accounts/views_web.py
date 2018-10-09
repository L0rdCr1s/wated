from django.shortcuts import render, get_object_or_404
from . import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, views
from django.core.mail import send_mail
import random, datetime
from django.utils import timezone
from .models import UserProfile, CustomUser


def homepage(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['email'], password=data['password'])

            if user is not None:
                if user.is_active:
                    request.session['username'] = data['email']
                    login(request, user)
                    return redirect('/accounts')
                else:
                    return HttpResponse('account is disabled')
            else:
                return HttpResponse('invalid username or password')
        else:
            return HttpResponse("invalid form")
    else:
        form = forms.LoginForm()
        return render(request, 'authentication/login.html', {'form': form})


def user_logout(request):
    views.logout(request)
    return render(request, 'authentication/logged_out.html')


def custom_user_register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])

            # creating activation key and save it together with the user
            activation_key = random.randint(1, 1000000)
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            user.activation_key=activation_key
            user.activation_key_expirity=key_expires
            user.save()

            email_subject = 'Your new site account confirmation'
            email_body = """Hello, %s, and thanks for signing up for an
            our site account!\n\nTo activate your account, click this link within 48
             hours:\n\nhttp://localhost:8000/accounts/confirm/%s""" % (
                form.cleaned_data['email'],
                user.activation_key)
            send_mail(email_subject,
                      email_body,
                      'miniacyclo@gmail.com',
                      [form.cleaned_data['email']])
            return redirect('/accounts/activate_account')
        else:
            # form = forms.RegisterForm()
            # return render(request, 'registration/register.html', {"form": form})
            return HttpResponse('invalid form')
    else:
        form = forms.RegisterForm()
        return render(request, 'registration/register.html', {"form": form})


def activate_account(request):
    return render(request, 'registration/activate_account.html')


def confirm_account(request, id):
    user = get_object_or_404(CustomUser, activation_key=id)
    if user is not None:
        now_aware = timezone.now()
        if user.activation_key_expirity < now_aware:
            message = 'the key is already expired'
            template = 'registration/activation_confirmed.html'
            return render(request, template, {'message': message})
        user.is_active = True
        user.save()
        return redirect('/accounts')
    else:
        message = 'this activation is not valid'
        template = 'registration/activation_confirmed.html'
        return render(request, template, {'message': message})


def reset_password_email(request):
    if request.method == 'POST':
        form = forms.PasswordReset(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(CustomUser, email=email)

            if user is not None:

                # creating activation key and save it together with the user
                activation_key = random.randint(1, 1000)
                key_expires = datetime.datetime.today() + datetime.timedelta(2)

                new_user = CustomUser.objects.get(user=user)
                new_user.activation_key = activation_key
                new_user.activation_key_expirity = key_expires
                new_user.save()

                email_subject = 'password reset form'
                email_body = """Hello, %s, click this link within to recover your password 24
                 hours:\n\nhttp://localhost:8000/accounts/resetmypassword/%s""" % (
                    user.email,
                    activation_key)

                send_mail(email_subject,
                          email_body,
                          'forums4ccount@gmail.com',
                          [form.cleaned_data['email']])
                message = 'the link to reset your password is sent to your account'
                template = 'authentication/password_reset_base.html'
                return render(request, template, {'message': message})
            else:
                return HttpResponse('user does not exist')
        else:
            return HttpResponse('form is not valid')
    else:
        form = forms.PasswordReset()
        return render(request, 'authentication/password_reset.html', {'form': form})


def reset_password(request, id):
    user = get_object_or_404(CustomUser, activation_key=id)
    if user is not None:
        now_aware = timezone.now()
        if user.activation_key_expirity < now_aware:
            message = 'the key is already expired'
            template = 'authentication/password_reset_base.html'
            return render(request, template, {'message': message})
        new_user = user.user
        if request.method == 'POST':
            form = forms.Newpassword(request.POST)
            if form.is_valid():
                new_user.set_password(form.cleaned_data['password2'])
                new_user.save()
                return redirect('/accounts/')
        else:
            form = forms.Newpassword()
            return render(request, 'registration/register.html', {'form': form})
        return redirect('/accounts')
    else:
        message = 'this activation is not valid'
        template = 'authentication/password_reset_base.html'
        return render(request, template, {'message': message})
