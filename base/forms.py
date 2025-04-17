from django import forms
from .models import Profile, Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'enrolled_courses']
        widgets = {
            'enrolled_courses': forms.CheckboxSelectMultiple()
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post...'}),
        }
