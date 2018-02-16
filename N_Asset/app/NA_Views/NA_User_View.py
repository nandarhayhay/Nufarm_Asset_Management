from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from NA_DataLayer.NA_User.models import User
from NA_DataLayer.NA_User.forms import UserLoginForm, UserRegistrationForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
def require_ajax(view):
    from functools import wraps
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view

class NA_User_Form(UserCreationForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
    'class':'form-control','placeholder':'Enter First Name'
    }))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={
    'class':'form-control','placeholder':'Enter Last Name'
    }))
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={
    'class':'form-control','placeholder':'Enter Username'
    }))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={
    'class':'form-control','placeholder':'Email Address'
    }))
    picture = forms.ImageField(required=False)
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={
    'class':'form-control','placeholder':'Password'
    }))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={
    'class':'form-control','placeholder':'Confirm Password'
    }))
    initializeForm_user = forms.CharField(required=False,widget=forms.HiddenInput())

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','picture','password1','password2')

def NA_User_Register(request):
    if request.method == 'POST':
        form = NA_User_Form(request.POST,request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            user_log = authenticate(username=user.email, password=password)
            return redirect('home')
    else:
        form = NA_User_Form()
        return render(request,'app/NA_User/NA_User_Register.html',{'form':form})

def login_view(request): # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect(request.GET.get('next'))
    else:
        title = "Login"
        formLogin = UserLoginForm(request.POST or None)
        if formLogin.is_valid():
            email = formLogin.cleaned_data.get("email")
            password = formLogin.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=email, password=password) 
            login(request, user)
            return redirect(request.GET.get('next'))
        context = {"formLogin":formLogin,
                   "title":title
        }

        return render(request, "app/layout.html", context)


def register_view(request):  #Creates a New Account & login New users
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Register"
        formReg = UserRegistrationForm(request.POST or None, request.FILES or None)
        if formReg.is_valid():
            user = formReg.save(commit=False)
            password = formReg.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("home")

        context = {"title":title, "formReg":formReg}

        return render(request, "app/NA_User/NA_User_Register.html", context)


def logout_view(request): # logs out the logged in users
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")


def user_profile(request, username=None): # updates User profile
    instance = get_object_or_404(User, username=username)
    if request.user.username != instance.username:
        from django.http import Http404
        raise Http404
    else:
        form = UserProfileUpdateForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            profile = form.save(commit=False)
            if profile.confirm_password != request.user.password1:
                messages.error(request, 'Password confirmation doesn\'t match')
            else:
                profile.email = email
                profile.save() # Saves the Updated Profile
                messages.success(request, 'Profile was Updated.')
                return redirect(profile.get_absolute_url())
        context = {
                  "form": form,
                  "title": "update"
                }
    return render(request, "app/NA_User/NA_User_Profile.html", context)