from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.authtoken import views as drf_auth

from accounts import views as account_view
from games import views

router = routers.DefaultRouter()
router.register(r'games/(?P<gameid>.+)/mods', views.GameModsViewSet, basename='mods')
router.register(r'games', views.GameViewSet, basename='games')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', drf_auth.obtain_auth_token),
    path('signup/', account_view.SignupApiView.as_view()),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Donkey Engine API",
            default_version='v1',
            contact=openapi.Contact(email="hello@donkey-engine.host"),
        ),
        public=True,
    )

    urlpatterns += [
        path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]

urlpatterns += router.urls
