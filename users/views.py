from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash

def login_required_decorator(func):
    return login_required(func, login_url='users:login')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('users:login')
# Create your views here.


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('moneymanager:home')
    return render(request, 'login.html')

@login_required_decorator
def home_page(request):
    return render(request, 'index.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration.html'


@login_required
def profile_page(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
            user.save()
            return redirect('users:login')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})