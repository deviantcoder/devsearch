from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, pagination
from django.contrib import messages


def projects(request):
    projects, search_query = search_projects(request)

    projects, custom_range, paginator = pagination(request, projects, results=3)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator,
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.user = request.user.profile
            review.save()

            project.get_vote_count

            messages.success(request, 'REVIEW WAS SUBMITTED')
            return redirect('project', pk)

    context = {
        'project': project,
        'form': form,
    }

    return render(request, 'projects/project.html', context)


@login_required(login_url='login')
def add_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def edit_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'project': project}

    return render(request, 'delete_template.html', context)
