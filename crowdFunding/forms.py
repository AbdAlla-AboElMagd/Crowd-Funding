from django import forms

from crowdFunding.models import ReportProject , ReportComment

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