from django.shortcuts import render, redirect
from . forms import UserRegisterForm, ProfileUpdateForm, UserInfoUpdateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main_app.models import Question, Answer

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
    ans_count = Answer.objects.filter(user=user1).count()
    context = {
        'user1' : user1,
        'question_count': question_count,
        'ans_count': ans_count,
    }
    return render(request, 'user/profile.html', context=context)


@login_required
def update_profile(request, username):
    if username == request.user.username:
        cur_user_obj = {
            'username': username,
            'email': request.user.email,
        }
        cur_user_profile = {
            'bio': request.user.profile.bio,
            'image': request.user.profile.image.url,
            'facebook_link': request.user.profile.facebook_link,
            'twitter_link': request.user.profile.twitter_link,
            'linkedin_link': request.user.profile.linkedin_link,
        }
        if request.method == "POST":
            user_update_form = UserInfoUpdateForm(request.POST, instance=request.user)
            profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_update_form.is_valid() and profile_update_form.is_valid():
                user_update_form.save()
                profile = profile_update_form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, f'Profile updated successfully')
                return redirect('profile_view', username=request.user.username)
        else:
            user_update_form = UserInfoUpdateForm(initial=cur_user_obj)
            profile_update_form = ProfileUpdateForm(initial=cur_user_profile)
        context = {
            'user_update_form': user_update_form,
            'profile_update_form': profile_update_form,
        }
        return render(request, 'user/update.html', context=context)
    else:
        return render(request, 'error.html')

