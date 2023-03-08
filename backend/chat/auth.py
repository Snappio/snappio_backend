from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_AUTH = JWTAuthentication()


@database_sync_to_async
def get_user(token: str):
    try:
        validated_token = JWT_AUTH.get_validated_token(token)
        return JWT_AUTH.get_user(validated_token)
    except Exception:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware that takes tokens from the header and populates the scope with the user
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        # find the authorization header
        headers = scope["headers"]
        user = AnonymousUser()
        token = None
        # get the token from the header
        for header in headers:
            if header[0] == b"authorization":
                token = header[1]
                break
        if token:
            token = token.split(b" ")[1]
            user = await get_user(token)
        scope["user"] = user

        return await self.app(scope, receive, send)
