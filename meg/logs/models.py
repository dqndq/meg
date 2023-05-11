from django.db import models


class ReadFileM(models.Model):
    file = models.FileField(
        'Файл',
        help_text='Перетащите сюда файл',
        upload_to='documents'
    )
