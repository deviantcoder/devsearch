from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, pagination


def profiles(request):
    profiles, search_query = search_profiles(request)

    profiles, custom_range, paginator = pagination(request, profiles, results=3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator,
    }

    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description__exact='')

    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }

    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'USER DOES NOT EXIST')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'LOGGED IN')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'USERNAME OR PASSWORD IS INCORRECT')

    page = 'login'

    context = {
        'page': page,
    }

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'LOGGED OUT')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            messages.success(request, 'USER ACCOUNT WAS CREATED')
            return redirect('edit_account')

    context = {
        'page': page,
        'form': form,
    }

    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}

    return render(request, 'users/edit_account.html', context)


@login_required(login_url='login')
def add_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form}

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def edit_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    context = {'object': skill}

    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messages_requests = profile.messages.all()
    unread_count = messages_requests.filter(is_read=False).count()

    context = {
        'messages_requests': messages_requests,
        'unread_count': unread_count,
    }

    return render(request, 'users/inbox.html', context)


def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if not message.is_read:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.user.is_authenticated:
        sender = request.user.profile
    else:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.first_name = sender.first_name
                message.last_name = sender.last_name
                message.email = sender.email

        message.save()

        messages.success(request, 'MESSAGE SENT')

        return redirect('profile', pk)

    context = {
        'form': form,
        'recipient': recipient,
    }

    return render(request, 'users/message_form.html', context)
