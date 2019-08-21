from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )

from django.shortcuts import render,redirect
from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('Loginview, Is the user ok? ' + str(request.user.is_authenticated()))
        return redirect('/')
    context = {'form':form,
               'title':title}
    return render(request, "login_form.html", context=context)

def register_view(request):
    print('Regview,Is the user auth? ' + str(request.user.is_authenticated()) + request.user.username)
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request,new_user)
        print('after valid/login. Is the user ok? ' + str(request.user.is_authenticated()) + request.user.username)
        return redirect('/')

    context = {'form': form,
               'title': title}

    return render(request, "login_form.html", context)

def logout_view(request):
    logout(request)
    return render(request, "login_form.html", {})

