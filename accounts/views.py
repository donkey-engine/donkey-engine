from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.request import Request

from accounts.serializers import AuthSerializer, SignupSerializer


class AuthApiView(generics.GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = ()

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return JsonResponse({
                'error': ['Bad credentials']
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            login(request, user)
            return JsonResponse({
                'id': user.pk,
                'username': user.get_username(),
            })


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = ()

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if User.objects.filter(username=validated_data['username']).exists():
            return JsonResponse(
                {'username': ['Already exists']},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        elif User.objects.filter(email=validated_data['email']).exists():
            return JsonResponse(
                {'email': ['Already exists']},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
            )
            return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)


def logout_view(request: Request):
    logout(request)
    return JsonResponse({'status': 'ok'})
