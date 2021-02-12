from django.contrib.auth.models import User
from rest_framework import generics

from accounts.serializers import SignupSerializer


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer_class()

        data = serializer(data=self.request.POST)
        data.is_valid(raise_exaption=True)

        name_new_user = request.POST.get('username')
        password_new_user = request.POST.get('password')
        email_new_user = request.POST.get('email')

        # if not User.objects.filter(Q(username=name_new_user) | Q(email=email_new_user)):

        if not User.objects.filter(username=name_new_user):
            if not User.objects.filter(email=email_new_user):
                user = User(username=name_new_user, password=password_new_user,
                            email=email_new_user)
                user.save()
