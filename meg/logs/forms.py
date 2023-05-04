from django import forms


class ReadFile(forms.Form):
    file = forms.CharField(label='Файл', help_text='Перетащите сюда файл', widget=forms.Textarea)
