from django.contrib.auth.models import User
from rest_framework import generics

from accounts.serializers import SignupSerializer


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer_class()

        data = serializer(data=self.request.POST)
        data.is_valid(raise_exaption=True)

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(Q(username=username) | Q(email=email)):
            user = User.objects.create_user(username, password, email)
            user.save()
