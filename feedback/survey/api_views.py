from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import Survey, QuestionAnswers
from .serializers import SurveySerializer, QuestionAnswerSerializer
import logging

logger = logging.getLogger(__name__)


class SurveyCreateView(generics.CreateAPIView):
    # Устанавливаем queryset для получения всех опросников из базы данных
    queryset = Survey.objects.all()
    # Указываем, какой сериализатор использовать для преобразования данных
    serializer_class = SurveySerializer
    # Устанавливаем права доступа: только авторизованные пользователи могут работать с этим API
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут создавать опросы

    def perform_create(self, serializer):
        # Передаем текущего пользователя в контекст запроса
        serializer.save(user_creator=self.request.user)


class SurveyDetailAndSubmitAPIView(RetrieveAPIView):
    queryset = Survey.objects.all()  # Базовый набор опросников
    serializer_class = SurveySerializer  # Сериализатор для преобразования данных
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get_queryset(self):
        # Возвращаем только те опросники, которые назначены текущему пользователю
        user = self.request.user
        return Survey.objects.filter(user_receiver=user)

    def post(self, request, *args, **kwargs):
        # Получаем объект опросника по ID из URL
        survey_id = kwargs.get('pk')  # 'pk' — параметр URL
        logger.info(f"Пользователь {request.user.username} пытается отправить ответы на опросник {survey_id}.")
        try:
            survey = self.get_queryset().get(id=survey_id)  # Проверяем, что опросник существует и доступен пользователю
        except Survey.DoesNotExist:
            return Response({"error": "Опросник не найден или недоступен."}, status=HTTP_400_BAD_REQUEST)

        # Извлекаем список ответов из данных запроса
        answers_data = request.data.get('answers', [])

        if not answers_data:
            logger.warning(f"Пользователь {request.user.username} не предоставил ответы для опросника {survey_id}.")
            return Response({"error": "Ответы не предоставлены."}, status=HTTP_400_BAD_REQUEST)

        # Получаем список вопросов из выбранного опросника
        questions = survey.questions.all()  # Все вопросы, связанные с опросником

        if not questions:
            logger.warning(f"У опросника {survey_id} нет вопросов.")
            return Response({"error": "У данного опросника нет вопросов."}, status=HTTP_400_BAD_REQUEST)

        # Проверяем, что количество ответов совпадает с количеством вопросов
        if len(answers_data) != questions.count():
            return Response(
                {"error": "Количество ответов не соответствует количеству вопросов."},
                status=HTTP_400_BAD_REQUEST
            )

        answers = []
        for question, answer_data in zip(questions, answers_data):
            value = answer_data.get('value')

            if not value:
                return Response(
                    {"error": f"Ответ для вопроса {question.id} не предоставлен."},
                    status=HTTP_400_BAD_REQUEST
                )

            # Создаем данные для каждого ответа
            answer_payload = {
                "question": question.id,  # Автоматически берем question_id из модели Questions
                "value": value
            }

            # Создаем экземпляр QuestionAnswerSerializer для каждого ответа
            serializer = QuestionAnswerSerializer(data=answer_payload, context=self.get_serializer_context())
            if serializer.is_valid():
                # Сохраняем ответ, связывая его с вопросом и пользователем
                answers.append(serializer.save())
            else:
                logger.error(f"Ошибка валидации ответа на вопрос {question.id}: {serializer.errors}")
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        # Преобразуем созданные ответы в JSON и возвращаем их
        serialized_answers = QuestionAnswerSerializer(answers, many=True, context=self.get_serializer_context())
        return Response(serialized_answers.data, status=HTTP_201_CREATED)


class UserSurveysListAPIView(ListAPIView):
    serializer_class = SurveySerializer  # Сериализатор для преобразования данных
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get_queryset(self):
        # Возвращаем только те опросники, которые назначены текущему пользователю
        user = self.request.user
        return Survey.objects.filter(user_creator=user)


class SurveyListWithAnswersAPIView(ListAPIView):
    serializer_class = SurveySerializer  # Сериализатор для преобразования данных
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get_queryset(self):
        # Фильтруем опросники по user_creator (текущий пользователь)
        user = self.request.user
        return Survey.objects.filter(user_creator=user).prefetch_related('questions__answers')

    def list(self, request, *args, **kwargs):
        # Получаем все опросы, созданные текущим пользователем
        surveys = self.get_queryset()

        # Сериализуем каждый опрос и добавляем ответы на вопросы
        response_data = []
        for survey in surveys:
            # Сериализуем опрос
            survey_serializer = self.get_serializer(survey)

            # Получаем все ответы на вопросы этого опросника
            answers = QuestionAnswers.objects.filter(question__survey=survey)
            answers_serializer = QuestionAnswerSerializer(answers, many=True)

            # Добавляем данные опросника и ответы в общий ответ
            response_data.append({
                'survey': survey_serializer.data,
                'answers': answers_serializer.data
            })
        # Возвращаем объединенный ответ
        return Response(response_data)