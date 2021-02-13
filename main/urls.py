from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as drf_auth

from accounts import views as account_view
from games import views

router = routers.DefaultRouter()
router.register(r'game', views.GameViewSet)
# Linking the API via automatic routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', drf_auth.obtain_auth_token),
    path('signup/', account_view.SignupApiView.as_view()),
]

urlpatterns += router.urls
