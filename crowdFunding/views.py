
from django.views import View
from django.views.generic import ListView

from crowdFunding.forms import ReportCommentModelForm, ReportProjectModelForm
from crowdFunding.models import Comment, Project, ReportProject, SelectedProject , User , ReportComment , Category , Tag

from django.db import models
from .models import Project, ProjectImage
from .forms import ProjectForm, ProjectImageForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from crowdFunding.forms import CustomUserCreationForm
from django.contrib import messages
from crowdFunding.models import User  
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.urls import reverse
def home(request):
    if request.session.get('email'):
        return render(request=request, template_name='crowdFunding/home.html')
    else:
        return redirect(custom_login)

def about(request):

    if request.session.get('email'):
        return render(request=request, template_name='crowdFunding/about.html')
    else:
        return redirect(custom_login)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # لسه مش مفعل
            user.save()

            # إعدادات الإيميل
            current_site = get_current_site(request)
            mail_subject = 'فعل حسابك الآن'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"
            
            message = render_to_string('crowdFunding/activation_email.html', {
                'user': user,
                'activation_url': activation_url
            })
            send_mail(mail_subject, message, 'drnasser.khairy@gmail.com', [user.email])

            messages.success(request, 'تم التسجيل! تحقق من بريدك الإلكتروني لتفعيل حسابك.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crowdFunding/signup.html', {'user_creation_form': form})

from django.contrib.auth import get_user_model

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تم تفعيل حسابك بنجاح! سجل دخولك الآن.')
        return redirect('login')
    else:
        messages.error(request, 'رابط التفعيل غير صالح أو انتهت صلاحيته.')
        return redirect('home')


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
    
#         if form.is_valid():
#             form.save()
           
#             messages.success(request, 'تم التسجيل بنجاح! سجل دخولك الآن.')  
#             return redirect(custom_login)  
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'crowdFunding/signup.html', {'user_creation_form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = user.email  
            return redirect('home')
        else:
            messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة!')

    return render(request, 'crowdFunding/login.html')
def custom_logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect(custom_login)
    
    
    
    
# def new(request):
#     form = UserForm()
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('home/')
#     return render(request=request, template_name='crowdFunding/register.html', context={'user_form': form})
    
# def signup(request):
#     user_creation_form = UserCreationForm()
#     if request.method == 'POST':
#         user_creation_form = UserCreationForm(request.POST)
#         if user_creation_form.is_valid():
#             user_creation_form.save()
#             user_name=user_creation_form.cleaned_data.get('username')
#             password=user_creation_form.cleaned_data.get('password1')
#             user=authenticate(username=user_name, password=password)
#             login(request, user)
#             return HttpResponseRedirect('home/')
#     context={
#             'user_creation_form': user_creation_form,
#     }
#     return render(request=request, template_name='crowdFunding/signup.html', context=context)
        
# def signup(request):
#     user_creation_form = CustomUserCreationForm()  # استخدام الفورم الجديد
#     if request.method == 'POST':
#         user_creation_form = CustomUserCreationForm(request.POST)
#         if user_creation_form.is_valid():
#             user = user_creation_form.save(commit=False)  # احفظ من غير ما تعمله save نهائي
#             user.is_active = True  # خليه نشط تلقائي
#             user.save()  # احفظ اليوزر
#             email = user_creation_form.cleaned_data.get('email')
#             password = user_creation_form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=password)  # التحقق بالإيميل والباسورد
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect('home/')
#     context = {
#         'user_creation_form': user_creation_form,
#     }
#     return render(request=request, template_name='crowdFunding/signup.html', context=context)











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

