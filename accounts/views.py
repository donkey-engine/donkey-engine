from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import exceptions, generics, status, views
from rest_framework.request import Request

from accounts.serializers import (AuthSerializer, ConfirmEmailSerializer,
                                  SignupSerializer)


EMAIL_TEMPLATE = """<h1>Please confirm your email for Donkey Engine account</h1>
<a href="https://donkey-engine.host/confirm_email/{token}">https://donkey-engine.host/confirm_email/{token}</a>"""


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


class ConfirmEmailView(generics.GenericAPIView):
    serializer_class = ConfirmEmailSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = self.request.user

        pass_gen = PasswordResetTokenGenerator()
        if not pass_gen.check_token(user=user, token=validated_data['token']):
            raise exceptions.PermissionDenied()
        user.profile.email_confirmed = True
        user.profile.save()
        return JsonResponse({'status': 'ok'})


class SendEmailConfirmationView(views.APIView):
    def post(self, request: Request):
        user = self.request.user

        if user.profile.email_confirmed:
            return JsonResponse({
                'error': 'Email already confirmed',
            }, status=status.HTTP_400_BAD_REQUEST)

        token = PasswordResetTokenGenerator().make_token(user=user)
        send_mail(
            'Email confirmation',
            None,
            None,
            [user.email],
            fail_silently=False,
            html_message=EMAIL_TEMPLATE.format(
                token=token,
            ),
        )

        return JsonResponse({
            'status': 'ok',
            'email': user.email,
        })


def logout_view(request: Request):
    logout(request)
    return JsonResponse({'status': 'ok'})
