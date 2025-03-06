from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import RegexValidator , MinLengthValidator , MaxLengthValidator , MinValueValidator , MaxValueValidator

from django.contrib.auth.models import AbstractUser, Group, Permission

from django.core.exceptions import ValidationError


egypt_phone_regex = RegexValidator(
    regex=r'^01[0125][0-9]{8}$',
    message="The Phone Number Must Be In The Format 01xxxxxxxx"
)

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200 , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='atachments/' , blank=True , null=True)
    phone = models.CharField(
        max_length=11,
        validators=[egypt_phone_regex],
        verbose_name="Must be Egyption Number"
    )
    is_staff = models.BooleanField(default=False)
    Birthdate= models.DateField(null=True , blank=True)
    facebook_profile = models.URLField(max_length=255 , null=True , blank=True)
    country = models.CharField(max_length= 255 , null=True , blank=True)

    groups = models.ManyToManyField(Group, related_name='crowdfunding_user_groups' , null=True , blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='crowdfunding_user_permissions', null=True , blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 


# class CustomUser(models.Model):
#     id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=False)
#     profile_pic = models.ImageField(upload_to='atachments/' , blank=True , null=True)
#     phone = models.CharField(
#         max_length=11,
#         validators=[egypt_phone_regex],
#         verbose_name="Must be Egyption Number"
#     )
#     isAdmin = models.BooleanField(default=False)
#     Birthdate= models.DateField(null=True , blank=True)
#     facebook_profile = models.URLField(max_length=255 , null=True , blank=True)
#     country = models.CharField(max_length= 255 , null=True , blank=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}" 
#
# projects



class Project(models.Model):

    class StateChoices(models.TextChoices):
        OPEN = "Open", "Open"
        IN_PROGRESS = "In Progress", "In Progress"
        DONE = "Done", "Done"
        CANCELLED = "Cancelled", "Cancelled"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    details = models.TextField()
    state = models.CharField(max_length=15, choices=StateChoices.choices, default=StateChoices.OPEN)
    attachment = models.FileField(blank=True , null=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_price = models.IntegerField()


    user = models.ForeignKey(User , on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    total_rating = models.FloatField(validators=[MinValueValidator(0,0) , MaxValueValidator(5.0)] , default=0.0)
    total_user_rated = models.IntegerField(default=0)


    def __str__(self):
        return self.title


    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return f"{self.project.title} Image"

   

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project , on_delete=models.CASCADE , related_name='tags')

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project , on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self' , on_delete=models.CASCADE , null=True , blank=True)
    is_parent = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text}"

class ReportProject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}: {self.text}"
    
class ReportComment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}: {self.text}"

class RatingProject(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.FloatField(validators=[MinValueValidator(0,0) , MaxValueValidator(5.0)])
    comment = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project , on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project_id', 'user_id')

class SelectedProject(models.Model):
    """
    This Model For the Admin to Select Only 5 projects to show in the Home Page 
    It Done by overriding the save method to check if the number of projects is less than 5 to save a new one
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project , on_delete=models.CASCADE , unique=True)


    def clean(self):
        if SelectedProject.objects.count() >= 5:
            raise ValidationError("You can select only 5 projects.")

    def save(self , *args , **kwargs):
        self.clean()
        if SelectedProject.objects.count() < 5:
            super().save(*args , **kwargs)
        else:
            raise ValidationError("You can select only 5 projects")
        
    def __str__(self):
        return f"{self.id}: {self.project}"
    

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} donated {self.amount} to {self.project}"
