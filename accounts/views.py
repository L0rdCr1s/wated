from django.shortcuts import get_object_or_404
from . import forms
from django.contrib.auth import authenticate, login, views
from django.core.mail import send_mail
import random, datetime
from django.utils import timezone
from .models import UserProfile, CustomUser, InstituteProfile, UserFollow
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from Sauti_yangu import shared
from sautiYangu.models import NotifyUser, Category


@api_view(['GET', ])
def homepage(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
def user_login(request):
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['email'], password=data['password'])

        if user is not None:
            if user.is_active:
                request.session['username'] = data['email']
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            elif user.activation_key == 1:
                user.is_active = True
                user.activation_key += random.randint(2, 1000000)
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def user_logout(request):
    views.logout(request)
    return Response(status=status.HTTP_410_GONE)


@api_view(['POST', ])
def custom_user_register(request):
    form = forms.RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password2'])

        # creating activation key and save it together with the user
        activation_key = random.randint(2, 1000000)
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
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def confirm_account(request, id):
    user = get_object_or_404(CustomUser, activation_key=id)
    if user is not None:
        now_aware = timezone.now()
        if user.activation_key_expirity < now_aware:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        user.is_active = True
        user.activation_key += random.randint(2, 1000000)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def reset_password_email(request):

    form = forms.PasswordReset(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = get_object_or_404(CustomUser, email=email)

        if user is not None:

            # creating activation key and save it together with the user
            activation_key = random.randint(2, 1000)
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
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET, POST, '])
def reset_password(request, id):
    user = get_object_or_404(CustomUser, activation_key=id)
    if user is not None:
        now_aware = timezone.now()
        if user.activation_key_expirity < now_aware:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        new_user = user.user
        if request.method == 'POST':
            form = forms.Newpassword(request.POST)
            if form.is_valid():
                new_user.set_password(form.cleaned_data['password2'])
                new_user.activation_key += random.randint(2, 1000000)
                new_user.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def update_password(request, pk):
    if request.user.is_authenticated():
        user = get_object_or_404(CustomUser, id=pk)
        if user.id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        form = forms.Newpassword(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password2'])
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserDetail(APIView):

    def get(self, request, pk):
        return shared.get_single(request, pk, CustomUser)

    def delete(self, request, pk):
        if request.user.is_authenticated():
            user = get_object_or_404(CustomUser, id=pk)
            if user.id != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
def deactivate_account(request):
    if request.user.is_authenticated():
        user = get_object_or_404(CustomUser, id=request.user.id)
        user.activation_key = 1
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserProfileList(APIView):

    def post(self, request):
        return shared.post(request, UserProfile, user='user')


class InstituteProfileList(APIView):

    def post(self, request):
        return shared.post(request, InstituteProfile, user='institute')


class UserProfileDetail(APIView):

    def get(self, request, pk):
        return shared.get_single(request, pk, UserProfile)

    def put(self, request, pk):
        serializer = shared.get_serializer(UserProfile, fields="__all__", rof=None)
        if request.user.is_authenticated():
            data = get_object_or_404(UserProfile, id=pk)
            if data.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            request.data['user'] = request.user.id
            serialized_data = serializer(data, data=request.data)

            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class InstituteProfileDetail(APIView):

    def get(self, request, pk):
        return shared.get_single(request, pk, InstituteProfile)

    def put(self, request, pk):
        serializer = shared.get_serializer(InstituteProfile, fields="__all__", rof=None)
        if request.user.is_authenticated():
            data = get_object_or_404(InstituteProfile, id=pk)
            if data.institute != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            request.data['institute'] = request.user.id
            serialized_data = serializer(data, data=request.data)

            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def follow(request, pk):
    if request.user.is_authenticated():
        followed = get_object_or_404(CustomUser, id=pk)
        if UserFollow.objects.filter(following=request.user, followed=followed).exist():
            UserFollow.objects.filter(following=request.user, followed=followed).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        follow = UserFollow.objects.create(following=request.user, followed=followed)
        follow.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def get_my_followers(request):
    if request.user.is_authenticated():
        followers = UserFollow.objects.filter(followed=request.user).order_by('-created_at')
        serializer = shared.get_serializer(UserFollow, fields="__all__", rof=None)
        return shared.serialize_many(followers, serializer)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def get_my_following(request):
    if request.user.is_authenticated():
        following = UserFollow.objects.filter(following=request.user).order_by('-created_at')
        serializer = shared.get_serializer(UserFollow, fields="__all__", rof=None)
        return shared.serialize_many(following, serializer)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def get_notifications(request):
    if request.user.is_authenticated():
        notifications = NotifyUser.objects.filter(target_user=request.user).order_by("read")
        serializer = shared.get_serializer(NotifyUser, fields='__all__', rof=None)
        return shared.serialize_many(notifications, serializer)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', ])
def update_notificaiton(request, pk):
    if request.user.is_authenticated():
        notification = get_object_or_404(NotifyUser, id=pk)
        notification.read = True
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def get_categories(request):
    return shared.get(request, Category, order_by='-name')
