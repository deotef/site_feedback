from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from survey.forms import AddSurveyForm, AddQuestionsFormSet
from survey.models import Questions, Survey


@login_required # Требует аутентификации пользователя
def add_survey(request):
    if request.method == "POST":
        # Создаем формы для данных из POST-запроса
        survey_form = AddSurveyForm(request.POST)
        formset = AddQuestionsFormSet(request.POST, instance=Survey())  # Привязываем формсет к новому Survey

        if survey_form.is_valid() and formset.is_valid():
            # Создаем объект Survey, но не сохраняем его в базу данных сразу
            survey = survey_form.save(commit=False)
            # Устанавливаем user_creator как текущего пользователя
            survey.user_creator = request.user
            survey.save()  # Сохраняем основной объект Survey
            # Обрабатываем ManyToMany-поле (если необходимо)
            survey_form.save_m2m()
            # Сохраняем связанные вопросы (Questions) и присваиваем им родительский опрос
            questions = formset.save(commit=False)  # Откладываем сохранение вопросов
            for question in questions:
                question.survey = survey  # Устанавливаем связь с созданным опросом
                question.save()  # Сохраняем каждый вопрос
            return redirect('users/')  # Перенаправление после успешного сохранения
    else:
        # Для GET-запроса создаем пустые формы
        survey_form = AddSurveyForm()
        formset = AddQuestionsFormSet(instance=Survey())  # Пустой формсет для новых вопросов
    return render(request, 'survey/add_survey.html', {'form': survey_form, 'formset': formset})


# Чтобы вывести все связанные с авторизованным пользователем (customuser_id = 3) опросы (survey_id = 2 и т.д.) в HTML-странице, вам нужно:
#
# Получить объект пользователя (например, request.user для текущего авторизованного пользователя).
# Использовать ManyToMany-связь, чтобы получить все связанные опросы.
# Передать эти данные в шаблон через контекст.
# Вывести их в HTML.
@login_required()
def list_surveys(request):
    # Получаем текущего авторизованного пользователя
    user = request.user
    # Используем related_name='UserReceiver', чтобы получить все связанные опросы
    surveys = user.UserReceiver.all()
    # Передаем опросы в контекст шаблона

    return render(request, 'survey/list_survey.html', {'surveys': surveys})