from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.forms import HhUserLoginForm, HhUserRegisterForm, HhUserEditForm, HhUserProfileEditForm
from authapp.renderers import UserJSONRenderer
from authapp.serializers import RegistrationSerializer, LoginSerializer


def login(request):
    login_form = HhUserLoginForm(data=request.POST or None)
    next_param = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        if 'next' in request.POST.keys():
            return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseRedirect(reverse('index'))
    context = {
        'login_form': login_form,
        'next': next_param,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = HhUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = HhUserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = HhUserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = HhUserProfileEditForm(request.POST, instance=request.user.hhuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = HhUserEditForm(instance=request.user)
        edit_profile_form = HhUserProfileEditForm(instance=request.user.hhuserprofile)
    context = {
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form,
    }
    return render(request, 'authapp/edit.html', context)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    # permission_classes = (AllowAny,)
    permission_classes =(AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        # print(request)
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

