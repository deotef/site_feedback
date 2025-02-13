from django.db import models
from django.db.models import CharField


# Create your models here.
class Role(models.Model):
    title = CharField(max_length=300)


    def __str__(self):
        return self.title