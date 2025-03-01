from django.db import models
from django.db.models import ForeignKey, CharField
from users.models import CustomUser


class Questions(models.Model):
    content = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey('QuestionType', on_delete=models.PROTECT, related_name='types', verbose_name="Типы" )
    survey = models.ForeignKey('Survey', on_delete=models.PROTECT, related_name='questions', default=1)


class QuestionType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class QuestionAnswers(models.Model):
    value = models.CharField(max_length=255)
    question = models.OneToOneField('Questions',on_delete=models.PROTECT, related_name='answers')
    user_return = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='UserCreator', default=1)
    user_receiver = models.ManyToManyField(CustomUser, related_name='UserReceiver')