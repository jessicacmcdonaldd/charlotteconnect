from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'enrolled_courses']
        widgets = {
            'enrolled_courses': forms.CheckboxSelectMultiple()
        }
