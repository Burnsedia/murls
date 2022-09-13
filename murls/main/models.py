from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.CharField(max_length=150, verbose_name=u"Aplikacja")
    link = models.URLField(verbose_name=u"Link do profilu")

class ProfileBiogram(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    biogram = models.CharField(max_length=350, verbose_name='Opis...', null=True)
    def __str__(self):
        return self.biogram

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name="Wgraj zdjęcie")


