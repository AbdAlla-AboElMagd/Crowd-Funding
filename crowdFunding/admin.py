
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

<<<<<<< HEAD

from .models import User , Tag , Project , Comment , ReportProject , ReportComment , RatingProject, Category, ProjectImage

from .models import SelectedProject, User , Tag , Project , Comment , ReportProject , ReportComment , RatingProject
=======
from .models import SelectedProject, User , Project , Comment , ReportProject , ReportComment , RatingProject , Category , Tag
>>>>>>> main


# from django.contrib.auth.models import User as DefaultUser

# # from .models import CustomUser

# # UnRegister Default User
# admin.site.unregister(DefaultUser)


# Custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'Birthdate', 'is_active', 'is_staff')

    # Fields to include in the add/edit forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'Birthdate', 'facebook_profile', 'country', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to include in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'Birthdate', 'facebook_profile', 'country', 'profile_pic'),
        }),
    )



# Register your models here.
# admin.site.register(User , UserAdmin)

admin.site.register(User, CustomUserAdmin)
# admin.site.register(CustomUser)

admin.site.register(Category)
admin.site.register(Project)
<<<<<<< HEAD
admin.site.register(Category)
admin.site.register(ProjectImage)
=======
admin.site.register(Tag)
>>>>>>> main
admin.site.register(Comment)
admin.site.register(ReportProject)
admin.site.register(ReportComment)
admin.site.register(RatingProject)
admin.site.register(SelectedProject)
