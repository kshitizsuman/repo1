from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    #print(request.user.is_authenticated())
    domain="http://"+request.META['HTTP_HOST']
    register=domain+"/register/"
    loginlink =domain+'/login/' 
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "form.html", {"message":"","form":form, "title": title , "register":register,"dashboard":domain,"loginlink":loginlink})


def register_view(request):
    domain="http://"+request.META['HTTP_HOST']
    register=domain+"/register/"
    loginlink =domain+'/login/'
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "message":"",
        "register":register,
        "dashboard":domain,
        "loginlink":loginlink,
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    domain="http://"+request.META['HTTP_HOST']
    register=domain+"/register/"
    loginlink =domain+'/login/'
    logout(request)
    return render(request, "form2.html", {"register":register,"dashboard":domain,"loginlink":loginlink})
    return redirect("/")
