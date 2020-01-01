# coding:utf-8

# 第三方模块Django内置模块
from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# 自定义模块
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class Login(View):
    template_name = 'dashboard/auth/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        to = request.GET.get('to', '')
        data = {'to': to}
        return render_to_response(request, self.template_name, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        to = request.GET.get('to', '')
        data = {}

        exists = User.objects.filter(username=username).exists()

        if not exists:
            data['error'] = "用户名错误"
            return render_to_response(request, self.template_name, data)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
        else:
            data['error'] = "密码错误"
            return render_to_response(request, self.template_name, data)

        if to:
            return redirect(to=to)
        return redirect(reverse('dashboard_index'))


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))


class AdminManger(View):
    template_name = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        data = {}

        users_list = User.objects.all()
        paginator = Paginator(users_list, 2)
        page = request.GET.get('page')
        data['page_range'] = paginator.page_range

        data['users'] = paginator.get_page(page)
        return render_to_response(request, self.template_name, data)


class UpdateAdminStatus(View):

    def get(self, request):
        username = request.GET.get('update_username')
        print(username)
        user = User.objects.filter(username=username).first()
        user.is_superuser = False if user.is_superuser else True
        user.save()
        print(user.is_superuser)
        return redirect(reverse('dashboard_admin_manger'))
