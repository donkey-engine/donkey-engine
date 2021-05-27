from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

from accounts.helpers.email import send_email_confirmation
from accounts.serializers import (AuthSerializer, ConfirmEmailSerializer,
                                  ResendEmailSerializer, SignupSerializer)


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
            try:
                user = User.objects.get(username=serializer.validated_data['username'])
            except User.DoesNotExist:
                return JsonResponse({
                    'error': ['Bad credentials']
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                if user.is_active is False:
                    return JsonResponse({
                        'error': ['User is inactive']
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
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
                is_active=False,
            )
            return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)


def logout_view(request: HttpRequest):
    logout(request)
    return JsonResponse({'status': 'ok'})


@api_view(['GET'])
@permission_classes([])
def resend_email_confirmation_view(request: Request):
    serializer = ResendEmailSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['username']

    if user.is_active:
        raise exceptions.ValidationError({'error': 'Email already confirmed'})

    send_email_confirmation(user)

    return JsonResponse({'status': 'ok'})


@api_view(['GET'])
@permission_classes([])
def confirm_email_view(request: Request):
    serializer = ConfirmEmailSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data['token']

    user = serializer.validated_data['username']
    pass_gen = PasswordResetTokenGenerator()
    if not pass_gen.check_token(user=user, token=token):
        raise exceptions.PermissionDenied()
    user.is_active = True
    user.save()
    return redirect(settings.LOGIN_PAGE)
