from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey

class Role(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name='Фотография', default='profile_pics/default.png')
    role = models.ForeignKey('Role', on_delete=models.PROTECT, default=3, related_name='roles', verbose_name="Роли")

    def __str__(self):
        return self.username