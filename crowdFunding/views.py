from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectForm, ProjectImageForm, ProjectImageFormSet
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request=request, template_name='crowdFunding/home.html')

def about(request):
    return render(request=request, template_name='crowdFunding/about.html')

from django.shortcuts import render, redirect
from .models import Project, ProjectImage
from .forms import ProjectForm, ProjectImageForm

def show_project(request):
    projects = Project.objects.all()
    return render(request, 'crowdFunding/project.html', {'projects': projects})



def add_project(request):
    picture_form = ProjectImageForm()
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        image_formset = ProjectImageFormSet(request.POST, request.FILES, queryset=ProjectImage.objects.none())


        if project_form.is_valid() and image_formset.is_valid():

            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            project_form.save_m2m()

            for form in image_formset:
                if form.cleaned_data.get('image'):
                    image = form.save(commit=False)
                    image.project = project
                    image.save()


            messages.success(request, "Project created successfully!")
            return redirect('show_project') 
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    
    else:
        project_form = ProjectForm()
        image_formset = ProjectImageFormSet(queryset=ProjectImage.objects.none())  

    return render(request, 'crowdFunding/add_project.html', {
        'project_form': project_form,
        'image_formset': image_formset,
    })


