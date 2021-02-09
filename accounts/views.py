from rest_framework import generics
from accounts.serializers import SignupSerializer


class SignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer_class()

        data = serializer(data=self.request.POST)
        data.is_valid(raise_exaption=True)

        username = request.POST.get('username')
        password = request.POST.get('username')
        if username and password:
            print("work")
