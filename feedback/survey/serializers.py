from rest_framework import serializers

from survey.models import Survey, Questions, QuestionAnswers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['content', 'type']


class SurveySerializer(serializers.ModelSerializer):
    # Добавляем вложенное поле questions для представления списка вопросов
    questions = QuestionSerializer(many=True)  # Параметр many=True указывает, что это список вопросов

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'user_creator', 'user_receiver', 'questions']  # Включаем title, description, user_receiver и список вопросов

    def create(self, validated_data):
        # validated_data — это словарь с проверенными данными из запроса
        # Мы извлекаем данные вопросов из validated_data
        questions_data = validated_data.pop('questions', [])  # Метод pop() удаляет ключ 'questions' из validated_data и возвращает его значение

        user_receiver_data = validated_data.pop('user_receiver', [])

        # Получаем текущего пользователя из контекста запроса
        user_creator = self.context['request'].user
        # Убедимся, что user_creator не передается дважды
        if 'user_creator' in validated_data:
            validated_data.pop('user_creator')

        # Создаем новый объект Survey, используя оставшиеся данные из validated_data
        # **validated_data — это распаковка словаря с данными для создания опросника
        survey = Survey.objects.create(user_creator=user_creator, **validated_data)

        # Устанавливаем user_receiver с помощью метода .set()
        survey.user_receiver.set(user_receiver_data)

        # Создаем связанные вопросы для созданного опросника
        for question in questions_data:  # Перебираем каждый вопрос из списка questions_data
            # Для каждого вопроса создаем новую запись в базе данных
            # survey — это созданный выше объект опросника
            # **question_data — это данные конкретного вопроса (например, content и type)
            Questions.objects.create(survey=survey, **question)


        # Возвращаем созданный объект Survey
        return survey


# {
#     "title": "Опрос о Django",
#     "description": "Этот опрос поможет нам улучшить Django.",
#     "user_receiver": [2, 3],  # Список ID пользователей-получателей
#     "questions": [
#         {
#             "content": "Как вам Django?",
#             "type": 1  # ID типа вопроса
#         },
#         {
#             "content": "Как часто вы используете Django?",
#             "type": 2
#         }
#     ]
# }


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswers
        fields = ['id', 'question', 'value']

    def create(self, validated_data):
        # Получаем текущего пользователя из контекста
        user = self.context['request'].user
        question = validated_data['question']  # Вопрос уже проверен в вьюхе

        # Создаем новый объект ответа
        answer = QuestionAnswers.objects.create(
            question=question,
            value=validated_data['value'],
            user_return=user  # Автоматически устанавливаем текущего пользователя
        )
        return answer

# Сервер получает объект опросника (Survey) по ID из URL (kwargs.get('pk')).
# Фильтрует вопросы, связанные с этим опросником (survey.questions.all()).
# Для каждого вопроса из списка questions создается словарь answer_payload, содержащий:
# question: ID вопроса (взят из модели Questions).
# value: Значение ответа, полученное из JSON-запроса.
# Эти данные передаются в QuestionAnswerSerializer для создания объекта ответа.
# {
#     "answers": [
#         {"value": "Отлично"},
#         {"value": "Каждый день"}
#     ]
# }