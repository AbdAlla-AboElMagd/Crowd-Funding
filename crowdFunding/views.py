from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.db import models
from crowdFunding.models import (
    Comment, Project, ReportProject, SelectedProject, User, 
    ReportComment, Category, Tag, Donation, ProjectImage
)
from crowdFunding.forms import (
    ReportCommentModelForm, ReportProjectModelForm, CustomUserCreationForm, 
    ProjectForm, ProjectImageForm, UserProfileForm
)
from .tokens import account_activation_token

# context = {}
# username =request.session.get("username" , None)
# context["username"] = username

def home(request):
    context = {}
    username = request.session.get("username" , None)
    context={"username":username}
    print(username)
    return render(request=request , template_name='crowdFunding/home.html' , context=context)

def about(request):

    if request.session.get('username'):
        username = request.session.get("username" , None)
        context={"username":username}
        return render(request=request, template_name='crowdFunding/about.html', context=context)
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




def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user:
            user.delete()
            logout(request)
            messages.success(request, 'تم حذف حسابك بنجاح!')
            return redirect('home')
        else:
            messages.error(request, 'كلمة المرور غير صحيحة!')
            return redirect('profile')


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




def custom_login(request):
     if not request.session.get('username'):
        username = request.session.get('username')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username  
                
                return redirect('home')
            else:
                messages.error(request, "username or Password Not Correct")

        return render(request, 'crowdFunding/login.html')
     else:
        return redirect('home')

def custom_logout(request):
    try:
        del request.session['username']
        logout(request)
    except:
        pass
    return redirect(custom_login)

# def update_profile(request):
#      if request.session.get('username'):
#         username = request.session.get('username')
#         if request.method == 'POST':
            
#             form = UserProfileForm(request.POST, request.FILES, instance=request.user, partial=True)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "تم تحديث بياناتك بنجاح!")
#             else:
#                 messages.error(request, "في خطأ في البيانات!")
#         else:
#             form = UserProfileForm(instance=request.user)
#         return render(request, 'crowdFunding/profile.html', {'form': form})
#      else:
#          return redirect("login")
def update_profile(request):
    if request.session.get('username'):
        username = request.session.get('username')
        if request.method == 'POST':
            user = request.user

            # احتفظ بالصورة القديمة لو مفيش صورة جديدة
            old_image = user.profile_image  # استخدم اسم الحقل بتاع الصورة هنا

            form = UserProfileForm(request.POST, request.FILES, instance=user, partial=True)
            if form.is_valid():
                profile = form.save(commit=False)
                
                # لو مفيش صورة جديدة، استخدم الصورة القديمة
                if not request.FILES.get('profile_image'):
                    profile.profile_image = old_image  # استخدم اسم الحقل بتاع الصورة هنا

                profile.save()
                messages.success(request, "تم تحديث بياناتك بنجاح!")
            else:
                messages.error(request, "في خطأ في البيانات!")
        else:
            form = UserProfileForm(instance=request.user)
        return render(request, 'crowdFunding/profile.html', {'form': form})
    else:
        return redirect("login")


def profile(request):
     if request.session.get('username'):
        username = request.session.get('username')
        # عرض المشاريع الخاصة باليوزر
        user_projects = Project.objects.filter(user=request.user)
        user_donations = Donation.objects.filter(user=request.user)  # لو عندك موديل اسمه Donation

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تحديث بروفايلك بنجاح!')
                return redirect('home')
        else:
            form = CustomUserCreationForm(instance=request.user)

        context = {
            "username":username,
            'form': form,
            'user': request.user,
            'projects': user_projects,
            'donations': user_donations,
        }
        return render(request, 'crowdFunding/profile.html', context)
     else:
        return redirect("home")
    
def show_project(request):
    projects = Project.objects.all()
    username = request.session.get('username',None)
    return render(request, 'crowdFunding/project.html', {'projects': projects, "username":username})

def add_project(request):
    if request.session.get('username'):
        username = request.session.get('username')
        if request.method == 'POST':
            project_form = ProjectForm(request.POST, request.FILES)
            image_form = ProjectImageForm(request.POST, request.FILES)

            if project_form.is_valid() and image_form.is_valid():
                # Save the project
                project = project_form.save(commit=False)
                project.user = User.objects.get(username=username)
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
            'username': username,
        })
    else:
        return redirect('login')
# Report Project CRUD Control
class CreateReportProject(View):
    def get(self , request , project_id):
        if request.session.get('username'):
            username = request.session.get('username')
            report_form = ReportProjectModelForm()
            context = {"report_form" : report_form , "project_id" : project_id,"username" : username}
            print( "Project_id :" , project_id)
            return render(request=request, template_name='crowdFunding/reportProject.html', context=context)
        else:
            return redirect('login')
    
    def post(self , request , project_id):
        if request.session.get('username'):
            username = request.session.get('username')
            report_form = ReportProjectModelForm(request.POST)

            if report_form.is_valid():
                print("title" , report_form.data['title'] )
                print( "Project_id :" , project_id)
                user = User.objects.get(username=username)
                project = Project.objects.get(id=project_id)
                report = ReportProject.objects.create(title = report_form.data['title'] , text=report_form.data['text'] , project = project , user = user)
                context = {"report_form" : report_form , "project_id" : project_id , "alert" : "success" , "message" : "Report Saved successfully","username" : username}
            else :
                context = {"report_form" : report_form , "project_id" : project_id , "alert" : "danger" , "message" : "Failed To Report Report","username" : username}
            return render(request=request, template_name='crowdFunding/reportProject.html', context=context)
        else:
            return redirect('login')

class UpdateReportProject(View):
    
    def get(self , request , report_id):
        if request.session.get('username'):
            username = request.session.get('username')
            report = ReportProject.objects.get(id = report_id)
            report_form = ReportProjectModelForm(instance=report)
            context = {"report_form" : report_form , "report_id" : report_id,"username" : username}
            return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)
        else:
            return redirect('login')
    
    def post(self , request , report_id):
        if request.session.get('username'):
            username = request.session.get('username')
            user = User.objects.get(username=username)

            report = ReportProject.objects.get(id = report_id)
            if report.user == user:
                report_form = ReportProjectModelForm(request.POST , instance=report)
                if report_form.is_valid():
                    report_form.save()
                    context = {"report_form" : report_form , "report_id" : report_id , "alert" : "success" , "message" : "Report updated successfully"}

                    return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)
                else:
                    context = {"report_form" : report_form , "report_id" : report_id , "alert" : "danger" , "message" : "Failed To Update The Report"}
                    return render(request=request, template_name='crowdFunding/upadteReportProject.html', context=context)
            else:
                return redirect('Home')
        else:
            return redirect('login')

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
        username = self.request.session.get("username", None)
        context['username'] = username
        return context
    
    # # Overriding the dispatch class to redirect to the login if not logged in
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('username'):
    #         return redirect('login')
    #     return super().dispatch(request, *args, **kwargs)
    
# Report Comment CRUD Control
class CreateReportComment(View):
    def get(self , request , comment_id):
        if request.session.get('username'):
            username = request.session.get('username')
            user = User.objects.get(username=username)
            report_form = ReportCommentModelForm()
            context = {"report_form" : report_form , "comment_id" : comment_id,"username" : username}
            # print( "comment_id :" , comment_id)
            return render(request=request, template_name='crowdFunding/reportComment.html', context=context)
        else:
            return redirect('login')
    
    def post(self , request , comment_id):
        if request.session.get('username'):
            username = request.session.get('username')
            
            report_form = ReportProjectModelForm(request.POST)

            if report_form.is_valid():
                print("title" , report_form.data['title'] )
                print( "comment_id :" , comment_id)
                user = User.objects.get(username=username)
                comment = Comment.objects.get(id=comment_id)
                report = ReportComment.objects.create(title = report_form.data['title'] , text=report_form.data['text'] , comment = comment , user = user)       
                context = {"report_form" : report_form , "comment_id" : comment_id  , "alert" : "success" , "message" : "Report Saved successfully"}
            else:
                context = {"report_form" : report_form , "comment_id" : comment_id  , "alert" : "danger" , "message" : "Failed To Save The Report"}

            return render(request=request, template_name='crowdFunding/reportComment.html', context=context)
        else :
            return redirect('login')


class UpdateReportComment(View):
    def get(self , request , report_id):
        if request.session.get('username'):
            username = request.session.get('username')
            user = User.objects.get(username=username)
            report = ReportComment.objects.get(id = report_id)
            if report.user == user :
                report_form = ReportCommentModelForm(instance=report)
                context = {"report_form" : report_form , "report_id" : report_id,"username" : username}
                return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)
            else :
                redirect('home')
        else:
            return redirect('login')
    
    def post(self , request , report_id):
        if request.session.get('username'):
            username = request.session.get('username')
            user = User.objects.get(username=username)
            report = ReportComment.objects.get(id = report_id)
            if report.user == user :
                report_form = ReportCommentModelForm(request.POST , instance=report)
                if report_form.is_valid():
                    report_form.save()
                    context = {"report_form" : report_form , "report_id" : report_id , "alert" : "success" , "message" : "Report updated successfully"}

                    return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)
                else:
                    context = {"report_form" : report_form , "report_id" : report_id , "alert" : "danger" , "message" : "Failed To Update The Report"}
                    return render(request=request, template_name='crowdFunding/upadteReportComment.html', context=context)
            else :
                return redirect('home')
        else:
            return redirect('login')

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
        username = self.request.session.get("username", None)
        context['username'] = username
        return context
    
    # # Overriding the dispatch class to redirect to the login if not logged in
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('username'):
    #         return redirect('login')
    #     return super().dispatch(request, *args, **kwargs)
    

def searchProject(request , search_text = None):
    context = {}
    if request.method == 'GET':
        search_text = request.GET.get('search' , '')
        if search_text:
            print("search_text" , search_text)
            context["search_text"] = search_text
            projects = Project.objects.filter(models.Q(title__icontains=search_text) | models.Q(details__icontains=search_text) | models.Q(tags__name__icontains=search_text)).distinct().order_by('id')
            context["projects"] = projects
            username = request.session.get("username" , None)
            context["username"] = username
            
    return render (request=request , template_name='crowdFunding/searchProject.html' , context=context)

def homepage(request):
    highest_rating = Project.objects.filter(state = "Open").order_by("-total_rating")[:5]
    selected_projects = SelectedProject.objects.all()
    latest_projects = Project.objects.all().order_by("-created_at")[:5]
    categories = Category.objects.all()
    username = request.session.get("username" , None)
    context = {"highest_rating" : highest_rating , "selected_projects" : selected_projects , "latest_projects" : latest_projects , "categories" : categories,"username":username}

    return render(request=request , template_name='crowdFunding/homepage.html' , context=context)

def projectInCategory(request , category_id):
    category = Category.objects.get(id=category_id)
    projects = Project.objects.filter(category=category)
    username = request.session.get("username" , None)
    context = {"projects" : projects , "category" : category, "username": username}
    return render(request=request , template_name='crowdFunding/projectInCategory.html' , context=context)

from django.db.models import F
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class DonateView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        form = DonationForm()
        return render(request, 'crowdFunding/donate.html', {'form': form, 'project': project})

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.project = project
            donation.save()

            # تحديث target_price بحيث ينقص بالمبلغ المتبرع به
            Project.objects.filter(id=project_id).update(target_price=F('target_price') - donation.amount)

            return redirect('project_detail', project_id=project.id)  # رجوع لصفحة المشروع بعد التبرع
        return render(request, 'crowdFunding/donate.html', {'form': form, 'project': project})

