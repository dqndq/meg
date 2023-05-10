from django import forms
from .models import ReadFile


class ReadFileForm(forms.ModelForm):
    class Meta:
        model = ReadFile
        fields = '__all__'
