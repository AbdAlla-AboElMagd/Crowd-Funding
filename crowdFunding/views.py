
from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectForm, ProjectImageForm
from django.contrib import messages


from django.shortcuts import render , redirect

from django.views import View
from django.views.generic import ListView

from crowdFunding.forms import ReportCommentModelForm, ReportProjectModelForm
from crowdFunding.models import Comment, Project, ReportProject, SelectedProject , User , ReportComment , Category , Tag

from django.db import models


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
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        image_form = ProjectImageForm(request.POST, request.FILES)

        if project_form.is_valid() and image_form.is_valid():
            # Save the project
            project = project_form.save(commit=False)
            project.user = request.user 
            project.save()
            project_form.save_m2m()  

            # Handle the main image (attachment)
            if 'attachment' in request.FILES:
                project.attachment = request.FILES['attachment']
                project.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                ProjectImage.objects.create(project=project, image=image)

            messages.success(request, "Project created successfully!")
            return redirect('project')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        project_form = ProjectForm()
        image_form = ProjectImageForm()

    return render(request, 'crowdFunding/add_project.html', {
        'project_form': project_form,
        'image_form': image_form,
    })

# Report Project CRUD Control
class CreateReportProject(View):
    def get(self , request , project_id):
        report_form = ReportProjectModelForm()
        context = {"report_form" : report_form , "project_id" : project_id}
        print( "Project_id :" , project_id)
        return render(request=request, template_name='crowdFunding/reportProject.html', context=context)
    
    def post(self , request , project_id):
        report_form = ReportProjectModelForm(request.POST)

        if report_form.is_valid():
            print("title" , report_form.data['title'] )
            print( "Project_id :" , project_id)
            user = User.objects.get(id=1)
            project = Project.objects.get(id=project_id)
            report = ReportProject.objects.create(title = report_form.data['title'] , text=report_form.data['text'] , project = project , user = user)
            context = {"report_form" : report_form , "project_id" : project_id , "alert" : "success" , "message" : "Report Saved successfully"}
        else :
            context = {"report_form" : report_form , "project_id" : project_id , "alert" : "danger" , "message" : "Failed To Report Report"}
        return render(request=request, template_name='crowdFunding/reportProject.html', context=context)


class UpdateReportProject(View):
    def get(self , request , report_id):
        report = ReportProject.objects.get(id = report_id)
        report_form = ReportProjectModelForm(instance=report)
        context = {"report_form" : report_form , "report_id" : report_id}
        return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)
    
    def post(self , request , report_id):
        report = ReportProject.objects.get(id = report_id)
        report_form = ReportProjectModelForm(request.POST , instance=report)
        if report_form.is_valid():
            report_form.save()
            context = {"report_form" : report_form , "report_id" : report_id , "alert" : "success" , "message" : "Report updated successfully"}

            return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)
        else:
            context = {"report_form" : report_form , "report_id" : report_id , "alert" : "danger" , "message" : "Failed To Update The Report"}
            return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)

class DeleteReportProject(View):
    def get(self , request , report_id):
        report = ReportProject.objects.get(id = report_id)
        report.delete()
        return redirect('ListReportProject')
    
class ListReportProject(ListView):
    model = ReportProject
    template_name = 'crowdFunding/listReportProject.html'
    context_object_name = 'reports'
    queryset = ReportProject.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    # # Overriding the dispatch class to redirect to the login if not logged in
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('username'):
    #         return redirect('login')
    #     return super().dispatch(request, *args, **kwargs)
    
# Report Comment CRUD Control
class CreateReportComment(View):
    def get(self , request , comment_id):
        report_form = ReportCommentModelForm()
        context = {"report_form" : report_form , "comment_id" : comment_id}
        # print( "comment_id :" , comment_id)
        return render(request=request, template_name='crowdFunding/reportComment.html', context=context)
    
    def post(self , request , comment_id):
        report_form = ReportProjectModelForm(request.POST)

        if report_form.is_valid():
            print("title" , report_form.data['title'] )
            print( "comment_id :" , comment_id)
            user = User.objects.get(id=1)
            comment = Comment.objects.get(id=comment_id)
            report = ReportComment.objects.create(title = report_form.data['title'] , text=report_form.data['text'] , comment = comment , user = user)       
            context = {"report_form" : report_form , "comment_id" : comment_id  , "alert" : "success" , "message" : "Report Saved successfully"}
        else:
            context = {"report_form" : report_form , "comment_id" : comment_id  , "alert" : "danger" , "message" : "Failed To Save The Report"}

        return render(request=request, template_name='crowdFunding/reportComment.html', context=context)


class UpdateReportComment(View):
    def get(self , request , report_id):
        report = ReportComment.objects.get(id = report_id)
        report_form = ReportCommentModelForm(instance=report)
        context = {"report_form" : report_form , "report_id" : report_id}
        return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)
    
    def post(self , request , report_id):
        report = ReportComment.objects.get(id = report_id)
        report_form = ReportCommentModelForm(request.POST , instance=report)
        if report_form.is_valid():
            report_form.save()
            context = {"report_form" : report_form , "report_id" : report_id , "alert" : "success" , "message" : "Report updated successfully"}

            return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)
        else:
            context = {"report_form" : report_form , "report_id" : report_id , "alert" : "danger" , "message" : "Failed To Update The Report"}
            return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)

class DeleteReportComment(View):
    def get(self , request , report_id):
        report = ReportComment.objects.get(id = report_id)
        report.delete()
        return redirect('ListReportComment')
    
class ListReportComment(ListView):
    model = ReportComment
    template_name = 'crowdFunding/listReportComment.html'
    context_object_name = 'reports'
    queryset = ReportComment.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    # # Overriding the dispatch class to redirect to the login if not logged in
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('username'):
    #         return redirect('login')
    #     return super().dispatch(request, *args, **kwargs)
    
    
# class SearchProject(ListView):
#     model = Project
#     template_name = 'crowdFunding/searchProject.html'
#     context_object_name = 'projects'
#     queryset = Project.objects.filter(models.Q(title__icontains='search_text') | models.Q(details__icontains='search_text') | models.Q(tags__name__icontains='search_text')).order_by('id')
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
def searchProject(request , search_text = None):
    context = {}
    if request.method == 'GET':
        search_text = request.GET.get('search' , '')
        if search_text:
            print("search_text" , search_text)
            context["search_text"] = search_text
            projects = Project.objects.filter(models.Q(title__icontains=search_text) | models.Q(details__icontains=search_text) | models.Q(tags__name__icontains=search_text)).distinct().order_by('id')
            context["projects"] = projects
    return render (request=request , template_name='crowdFunding/searchProject.html' , context=context)

def homepage(request):
    highest_rating = Project.objects.filter(state = "Open").order_by("-total_rating")[:5]
    selected_projects = SelectedProject.objects.all()
    latest_projects = Project.objects.all().order_by("-created_at")[:5]
    categories = Category.objects.all()

    context = {"highest_rating" : highest_rating , "selected_projects" : selected_projects , "latest_projects" : latest_projects , "categories" : categories}

    return render(request=request , template_name='crowdFunding/homepage.html' , context=context)

def projectInCategory(request , category_id):
    category = Category.objects.get(id=category_id)
    projects = Project.objects.filter(category=category)
    context = {"projects" : projects , "category" : category}
    return render(request=request , template_name='crowdFunding/projectInCategory.html' , context=context)
