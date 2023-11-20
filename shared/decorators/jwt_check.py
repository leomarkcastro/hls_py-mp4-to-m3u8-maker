from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
JWT_authenticator = JWTAuthentication()

# create a decorator that checks for jwt token


def jwt_check(func):
    def wrapper(request, *args, **kwargs):
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user, token = response
            request.user = user
            return func(request, *args, **kwargs)
        else:
            # return 401 if no token is provided
            return HttpResponse(b"You are not authorized to view this page.", status=401)
    return wrapper
