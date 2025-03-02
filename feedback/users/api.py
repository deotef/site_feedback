from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from . import serializers
from . import models


class CustomUserAPIList(ListAPIView):
    serializer_class = serializers.CustomUserListSerializer

    def get_queryset(self):
        return models.CustomUser.objects.all()


class CustomUserAPIPost(CreateAPIView):
    serializer_class = serializers.CustomUserSerializer

# class CustomUserRegistrationView(APIView): 2 способ
#     def post(self, request):
#         serializer = serializers.CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#               "message": "User registered successfully"
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserAPIDestroy(RetrieveDestroyAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserListSerializer
    permission_classes = (IsAdminUser, )


class CustomUserAPIUpdate(RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем текущего аутентифицированного пользователя
        return self.request.user
