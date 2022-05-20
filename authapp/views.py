from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.forms import HhUserLoginForm, HhUserRegisterForm, HhUserEditForm, HhUserProfileEditForm, SkillEditForm, \
    SkillCreateForm, UserSkillsForm
from authapp.models import HhUser, Skills, HhUserProfile
from authapp.serializers import HhUserSerializer


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def login(request):
    """Страница логина"""
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
    """Страница логаута"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """Страница регистрации новаго пользователя"""
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
    """Изменение пользователя"""
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


@login_required
def personal_account(request):
    """Личный кабинет"""
    context = {
        'title': 'Главная',
        'account': HhUserProfile.objects.get(pk=request.user.id),
    }
    return render(request, 'authapp/personal_account.html', context)


@login_required
def skills_add(request):
    """Страница с добавлением навыков"""
    if request.method == 'POST' and 'add_user_skill' in request.POST:
        user_skills_form = UserSkillsForm(request.POST, request.FILES, instance=request.user)
        if user_skills_form.is_valid():
            user_skills_form.save()
    else:
        user_skills_form = UserSkillsForm(instance=request.user)
    if request.method == 'POST' and 'add_skill' in request.POST:
        skill_form = SkillCreateForm(request.POST)
        if skill_form.is_valid():
            skill_form.save()
    else:
        skill_form = SkillCreateForm()
    context = {
        'title': 'Главная',
        'account': HhUser.objects.get(pk=request.user.id),
        'skill_form': skill_form,
        'user_skills_form': user_skills_form,
    }
    return render(request, 'authapp/skills_add.html', context)


"""Далее CRUD для скилов, доступен только для суперпользователя"""
class SkillCreateView(AccessMixin, CreateView):
    model = Skills
    template_name = 'authapp/skills/skill_form.html'
    success_url = reverse_lazy('authapp:skills_list')
    form_class = SkillCreateForm


class SkillsListView(AccessMixin, ListView):
    model = Skills
    template_name = 'authapp/skills/skills.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Skills.objects.all()
        return context_data


class SkillUpdateView(AccessMixin, UpdateView):
    model = Skills
    template_name = 'authapp/skills/skill_form.html'
    success_url = reverse_lazy('authapp:skills_list')
    form_class = SkillEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


class SkillDeleteView(AccessMixin, DeleteView):
    model = Skills
    template_name = 'authapp/skills/skill_delete.html'

    def get_success_url(self):
        return reverse('authapp:skills_list')
""" CRUD skills"""


class HhUserCreateAPIView(APIView):
    """Создание пользователя"""
    def get(self, request):
        item = HhUser.objects.all()
        serializer = HhUserSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HhUserSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HhUserUpdateAPIView(APIView):
    """Изменение пользователя"""
    def get_object(self, pk):
        try:
            return HhUser.objects.get(pk=pk)
        except HhUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = HhUserSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = HhUserSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

