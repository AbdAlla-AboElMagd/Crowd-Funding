
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag, Project, Comment, ReportProject, ReportComment, RatingProject, SelectedProject, Category

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(ReportProject)
admin.site.register(ReportComment)
admin.site.register(RatingProject)
admin.site.register(SelectedProject)
