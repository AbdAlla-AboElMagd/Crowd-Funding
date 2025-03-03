from django.shortcuts import render , redirect

from django.views import View
from django.views.generic import ListView

from crowdFunding.forms import ReportCommentModelForm, ReportProjectModelForm
from crowdFunding.models import Comment, Project, ReportProject , User , ReportComment

# Create your views here.
def home(request):
    return render(request=request, template_name='crowdFunding/home.html')

def about(request):
    return render(request=request, template_name='crowdFunding/about.html')

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
    
    