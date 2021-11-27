from django.http import JsonResponse
from django.http.request import HttpRequest


def healthcheck(request: HttpRequest):
    return JsonResponse({"status": "success"})
