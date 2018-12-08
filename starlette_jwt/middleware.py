import jwt
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, BaseUser, AuthCredentials
)


class JWTUser(BaseUser):
    def __init__(self, username: str, token: str, payload: dict) -> None:
        self.username = username
        self.token = token
        self.payload = payload

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username


class JWTAuthenticationBackend(AuthenticationBackend):

    def __init__(self, secret_key: str, prefix: str = 'JWT', username_field: str = 'username'):
        self.secret_key = secret_key
        self.prefix = prefix
        self.username_field = username_field

    @classmethod
    def get_token_from_header(cls, authorization: str, prefix: str):
        """
        Parses the Authorization header and returns only the token

        :param authorization:
        :return:
        """
        if authorization is None:
            raise AuthenticationError('Authorization header is missing')
        try:
            scheme, token = authorization.split()
        except ValueError:
            raise AuthenticationError('Could not separate Authorization scheme and token')
        if scheme.lower() != prefix.lower():
            raise AuthenticationError(f'Authorization scheme {scheme} is not supported')
        return token

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        token = self.get_token_from_header(authorization=auth, prefix=self.prefix)
        try:
            payload = jwt.decode(token, key=self.secret_key)
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(str(e))

        return AuthCredentials(["authenticated"]), JWTUser(username=payload[self.username_field], token=token,
                                                           payload=payload)
