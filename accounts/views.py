import typing as t
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import exceptions, generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from accounts.helpers.email import send_email_confirmation
from accounts.helpers.user import (EmailAlreadyExists, UsernameAlreadyExists,
                                   discord_signup, signup)
from accounts.serializers import (AuthSerializer, ConfirmEmailSerializer,
                                  DiscordRedirectSerializer,
                                  ResendEmailSerializer, SignupSerializer)
from common.clients.ws import get_user_room


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

        try:
            signup(validated_data['username'],
                   validated_data['password'],
                   validated_data['email'])
        except UsernameAlreadyExists:
            return JsonResponse(
                {'username': ['Already exists']},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except EmailAlreadyExists:
            return JsonResponse(
                {'email': ['Already exists']},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)


class DiscordAuthView(viewsets.ViewSet):
    permission_classes = ()

    class TokenInfo(t.TypedDict):
        access_token: str
        token_type: str
        expires_in: int
        refresh_token: str
        scope: str

    class CurrentUser(t.TypedDict):
        id: str
        username: str
        email: str

    @action(detail=False)
    def discord(self, request: Request):
        url_path = reverse('discord-auth-redirect')
        query = {
            'response_type': 'code',
            'client_id': settings.DISCORD_CLIENT_ID,
            'scope': 'identify email',
            'redirect_uri': settings.HOST_NAME + url_path
        }
        url = f'{settings.DISCORD_AUTHORIZATION_URL}?{urlencode(query)}'
        return redirect(url)

    @action(detail=False, url_path='discord/redirect')
    def redirect(self, request: Request):
        serializer = DiscordRedirectSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        token_info = self.exchange_code(code)
        access_token = token_info['access_token']

        current_user = self.get_current_user(access_token)
        # TODO: handle already existed username
        user = discord_signup(username=current_user['username'],
                              email=current_user['email'],
                              discord_id=current_user['id'])
        login(request, user)
        return redirect(settings.LOGIN_PAGE)

    def exchange_code(self, code: str) -> TokenInfo:
        url_path = reverse('discord-auth-redirect')
        data = {
            'client_id': settings.DISCORD_CLIENT_ID,
            'client_secret': settings.DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.HOST_NAME + url_path
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(settings.DISCORD_TOKEN_URL, data=data, headers=headers)
        return response.json()

    def get_current_user(self, access_token: str) -> CurrentUser:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{settings.DISCORD_API_URL}/users/@me', headers=headers)
        return response.json()


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


@api_view(http_method_names=['GET'])
@permission_classes((IsAuthenticated,))
def get_me(request: Request):
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'websocket_room': get_user_room(request.user.id, extend=True).hex,
    })
