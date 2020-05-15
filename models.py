from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate(value):
    if value<0 or value > 15:
        raise ValidationError(
            _('Incorrect Value Selected'),
            params={'value': value},
        )



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="Blank_Profile_Pic.jpg", upload_to="_profile_pics_")

    def __str__(self):
        return f'{self.user.username} Profile'


class Album(models.Model):
    FORMAT_CHOICES = [('Vinyl', 'Vinyl'), ('CD', 'CD'), ('Cassette', 'Cassette')]

    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    key = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    Format = models.CharField(max_length=15, choices=FORMAT_CHOICES, default="Vinyl")

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.album_title + ' - ' + self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    date_released = models.CharField(max_length=10, default="DD-MM-YYYY")
    length =models.CharField(max_length=5, default='0:00')
    #file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    Box = models.IntegerField(null=False, validators=[validate])
    Track_num = models.IntegerField(null=False)
    #is_favorite = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('music:index')

    def __str__(self):
        return self.song_title
