from django import forms
from .models import Project, ProjectImage, Tag

class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False,
    label="Tags"
)
    
    class Meta:
        model = Project
        fields = '__all__'
        fields = ['title', 'state', 'deadline', 'target_price','tags']
       
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control shadow-sm border-primary',
                'placeholder': 'Enter the title',
                'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            }),
            # 'category': forms.TextInput(attrs={
            #     'class': 'form-control shadow-sm border-primary',
            #     'placeholder': 'Enter the category',
            #     'style': 'border-radius: 10px; border: 1px solid #586F6B; padding: 10px;'
            # }),
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
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}) # Single file input
        }

ProjectImageFormSet = forms.modelformset_factory(
    ProjectImage,
    form=ProjectImageForm,
    extra=3,  # Number of empty forms to display
    can_delete=True  # Allow users to delete images
)
