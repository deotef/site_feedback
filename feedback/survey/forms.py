from django import forms
from django.forms import inlineformset_factory

from survey.models import Survey, Questions


class AddSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'user_receiver']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class AddQuestionsForSurvey(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['content', 'type']


# Создаем формсет — это механизм, который позволяет отображать и обрабатывать несколько форм одного типа на одной странице.
# Создаем inline формсет для связи Questions с Survey
AddQuestionsFormSet = inlineformset_factory(
    Survey,
    Questions,
    form=AddQuestionsForSurvey,
    extra=5, #Это количество дополнительных пустых форм, которые будут отображаться на странице.
    can_delete=True, #Добавляет флажок "удалить" для каждой формы, чтобы пользователь мог удалять существующие вопросы или нет необходимости создавать больше.
)