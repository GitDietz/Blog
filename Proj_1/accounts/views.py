from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

from django.shortcuts import render
from .forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('Is the user ok? ' + str(request.user.is_authenticated()))

    context = {'form':form,
               'title':title}
    return render(request, "login_form.html", context=context)

def register_view(request):
    return render(request, "form.html", {})

def logout_view(request):
    return render(request, "form.html", {})
