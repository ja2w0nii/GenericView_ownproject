from django.shortcuts import render
import jwt
import requests
from django.core.exceptions import PermissionDenied
from http import HTTPStatus
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from users.models import User


# session 로그인 여부 확인
# class AuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if (
#             not request.user.is_authenticated
#             and request.path != "/users/signin/"
#             and request.path != "/users/signup/"
#             and request.path != "/accounts/keycloak/login/"
#             and request.path != "/accounts/keycloak/login/callback/"
#             and "admin" not in request.path
#         ):
#             return redirect("/users/signin/")
#         response = self.get_response(request)
#         return response


# token 로그인 여부 확인
class JsonWebTokenMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if (
                request.path != "/users/signup/"
                and request.path != "/users/signin/"
                and request.path != "/keycloak/login/"
                and request.path != "/keycloak/login/callback/"
                and request.path != "/accounts/keycloak/login/"
                and request.path != "/accounts/keycloak/login/callback/"
                and "admin" not in request.path
            ):
                access_token = request.COOKIES.get("access_token")

                if not access_token:
                    raise PermissionDenied()

                # token = AccessToken(access_token)
                # email = token.payload.get("email")

                # if not email:
                #     raise PermissionDenied()
                # User.objects.get(email=email)

            response = self.get_response(request)

            return response

        except (PermissionDenied, User.DoesNotExist):
            return render(request, "signin.html", status=HTTPStatus.UNAUTHORIZED)
        except TokenError:
            return render(request, "signin.html", status=HTTPStatus.FORBIDDEN)
