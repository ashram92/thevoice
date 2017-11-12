from django.contrib.auth import authenticate, login, logout
from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from voice_app.accounts.models import User


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = tuple()

    def post(self, request, *args, **kwargs):
        user = self.validate(request.data)
        login(request, user)
        return Response(status=status.HTTP_201_CREATED)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username:
            raise ValidationError('NO_USERNAME')
        if not password:
            raise ValidationError('NO_PASSWORD')

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('INVALID_CREDENTIALS')
        return user


class UserLogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_admin',
            'is_mentor',
        )

    is_admin = serializers.BooleanField(source='is_superuser')


class ProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
