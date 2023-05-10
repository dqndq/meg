from django.db import models


class ReadFile(models.Model):
    file = models.FileField('Файл', help_text='Перетащите сюда файл', upload_to='documents/')
