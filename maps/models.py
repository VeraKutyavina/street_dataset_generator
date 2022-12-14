from django.db import models


class Screenshot(models.Model):
    screenshot = models.ImageField(upload_to='img/screenshots/', help_text='Html2canvas screenshot')
