from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.request import Request

from accounts.serializers import SignupSerializer


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = ()

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name_new_user = serializer.validated_data['username']
        password_new_user = serializer.validated_data['password']
        email_new_user = serializer.validated_data['email']

        if User.objects.filter(Q(username=name_new_user) | Q(email=email_new_user)):
            return JsonResponse({'status': 'error'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            user = User(username=name_new_user, password=password_new_user,
                        email=email_new_user)
            user.save()
            return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)
