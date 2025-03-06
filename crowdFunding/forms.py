from django import forms
from .models import Project, ProjectImage, Tag
from django.contrib.auth.forms import UserCreationForm
from crowdFunding.models import User, ReportProject, ReportComment
# فورم لإنشاء مستخدم جديد
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'profile_pic')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'Birthdate', 'country', 'facebook_profile', 'profile_pic']
    
    # جعل الفيلدز اختيارية
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags"
    )

    class Meta:
        model = Project
        fields = ['title', 'state', 'deadline', 'target_price', 'tags', 'details', 'attachment']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control shadow-sm border-primary',
                'placeholder': 'Enter the title',
                'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control bg-light',
                'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            }),
            'target_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the target price',
                'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the details',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Main Image'
            }),
        }

class ProjectImageForm(forms.ModelForm):
    images = MultipleFileField(label='Additional Images', required=False)

    class Meta:
        model = ProjectImage
        fields = ['images']




class userForm(forms.Form):
    username = forms.CharField(max_length=25 , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Username'}) ) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}))

class ReportProjectModelForm(forms.ModelForm):
    class Meta:
        model = ReportProject
        fields = "__all__"
        exclude= ['id' , 'created_at' , 'updated_at' , 'user' , 'project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Report Title' , 'required': True}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Report Description', 'required': True}),
        }
class ReportCommentModelForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = "__all__"
        exclude= ['id' , 'created_at' , 'updated_at' , 'user' , 'comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Report Title', 'required': True}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Report Description', 'required': True}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a comment...'})
        }

from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter donation amount'})
        }

