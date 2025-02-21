from django.db import models
from django.db.models import ForeignKey, CharField
from users.models import CustomUser


class Questions(models.Model):
    content = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    type = models.ForeignKey('QuestionType', on_delete=models.PROTECT, related_name='types', verbose_name="Типы" )


class QuestionType(models.Model):
    title = models.CharField(max_length=255)


class QuestionAnswers(models.Model):
    content = models.CharField(max_length=255)
    question = models.OneToOneField('Questions',on_delete=models.PROTECT, related_name='QuestionToUser')
    user_return = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='UserReturn')


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    question = models.ForeignKey(Questions, on_delete=models.PROTECT, related_name='Question')
    user_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='UserCreator')