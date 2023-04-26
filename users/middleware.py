from django.shortcuts import redirect


# 로그인 여부 확인
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and request.path != "/users/signin/"
            and request.path != "/users/signup/"
            and request.path != "/admin/"
        ):
            return redirect("/users/signin/")
        response = self.get_response(request)
        return response
