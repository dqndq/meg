from django import forms
from .models import ReadFileM


class ReadFileForm(forms.ModelForm):
    class Meta:
        model = ReadFileM
        fields = '__all__'
