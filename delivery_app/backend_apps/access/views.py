from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash)
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
# from ..forms.RegistroForm import RegistroForm
from .forms import UserLoginForm


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        # Roles estaticos estudiante y administrador

        # return redirect("/dashboard")
        return redirect("/")

    return render(request, "access/login.html", {"form": form, "title": title})


def home(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)

    return render(request, "access/home.html", {'form': form})


@login_required
def dashboard(request):
    return render(request, "access/dashboard.html")


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su contraseña fue cambiada satisfactoriamente!')
            return redirect('access:change_password')
        else:
            messages.error(request, 'Corrija por favor el error abajo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'access/change_password.html', {
        'form': form
    })
