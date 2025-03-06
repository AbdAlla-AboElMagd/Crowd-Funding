"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from crowdFunding.views import CreateReportComment, CreateReportProject, DeleteReportComment, DonateView, ListReportComment, ListReportProject, UpdateReportComment, UpdateReportProject, DeleteReportProject , about, add_comment, add_project, delete_comment, home, homepage, project_details, projectInCategory, searchProject, show_project, update_comment
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home , name ='home'),
    # path('home/' , home , name='home'),
    path('about/' , about , name='about'),
    path('project/' , show_project , name='project'),
    path('add_project/' , add_project , name='add_project'),
    path('project/<int:project_id>/', project_details, name='project'),
    path('project/<int:project_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('comment/update/<int:comment_id>/', update_comment, name='update_comment'),
    path('project/<int:project_id>/donate/', DonateView.as_view(), name='donate_project'),
    path('report_project/<int:project_id>/', CreateReportProject.as_view(), name='report_project'),
    path('report_comment/<int:comment_id>/', CreateReportComment.as_view(), name='report_comment'),
    # Report Project
    path('reportProject/<int:project_id>' , CreateReportProject.as_view() , name='reportProject'),
    path('updateReportProject/<int:report_id>' , UpdateReportProject.as_view() , name='UpdateReportProject'),
    path('deleteReportProject/<int:report_id>' , DeleteReportProject.as_view() , name='DeleteReportProject'),
    path('ListReportProject/' , ListReportProject.as_view() , name='ListReportProject'),
    # Report Comment
    path('reportComment/<int:comment_id>' , CreateReportComment.as_view() , name='reportComment'),
    path('updateReportComment/<int:report_id>' , UpdateReportComment.as_view() , name='UpdateReportComment'),
    path('deleteReportComment/<int:report_id>' , DeleteReportComment.as_view() , name='DeleteReportComment'),
    path('ListReportComment/' , ListReportComment.as_view() , name='ListReportComment'),

    # Search Urls
    # path('searchProject/' , searchProject , name='searchProjectNoText'),
    path('searchProject/' , searchProject , name='searchProject'),

    #homepage
    path('home/' , homepage , name='home'),

    #Project In Category
    path('category/<int:category_id>' , projectInCategory , name='category'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
