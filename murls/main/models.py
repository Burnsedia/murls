from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime

class ProfileLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.CharField(max_length=150, verbose_name=u"Aplikacja")
    link = models.URLField(verbose_name=u"Link do profilu")


class ProfileBiogram(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    biogram = models.CharField(max_length=350, verbose_name='Opis...', null=True)

    def __str__(self):
        return self.biogram


def user_avatars_directory(Avatar, filename):
    date_object = datetime.date.today()
    return "users/{}/{}/{}".format(Avatar.user, date_object, Avatar.avatar)


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatars_directory, blank=True, null=True, verbose_name="Wgraj zdjęcie")

    def save(self, *args, **kwargs):
        super(Avatar, self).save()
        img = Image.open(self.avatar.path)

        if img.height > 500 or img.width > 500:
            output_size = (400, 400)
            img.thumbnail(output_size)
            exif = img.getexif()
            img.save(self.avatar.path, exif=exif, quality=80)