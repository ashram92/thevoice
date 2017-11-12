from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


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
