from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main_app.models import Question
# Create your views here.


def login(request):
    return redirect('login')


def logout(request):
    logout(request)
    return redirect('logout')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created sucessfully for {username}. Login now")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form})


@login_required
def profile_view(request, username):
    user1 = User.objects.get(username=username)
    question_count = Question.objects.filter(user=user1).count()
    context = {
        'user1' : user1,
        'question_count': question_count,
    }
    return render(request, 'user/profile.html', context=context)