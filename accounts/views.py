from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.request import Request

from accounts.serializers import SignupSerializer


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request: Request):
        serializer = self.get_serializer_class()

        data = serializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.validated_data

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
            User.objects.create(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
            )
            return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)
