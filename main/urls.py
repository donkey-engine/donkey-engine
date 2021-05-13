from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from accounts import views as account_views
from games import views as games_views
from servers import views as servers_views

router = routers.DefaultRouter()
router.register(r'api/games/(?P<game_id>.+)/mods', games_views.GameModViewSet, basename='mods')
router.register(r'api/games', games_views.GameViewSet, basename='games')
router.register(r'api/servers', servers_views.ServersViewSet, basename='servers')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', account_views.AuthApiView.as_view()),
    path('api/signup/', account_views.SignupApiView.as_view()),
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
