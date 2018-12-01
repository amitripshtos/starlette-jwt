from starlette.requests import Request, Headers
from starlette.exceptions import HTTPException
import jwt
from starlette.responses import JSONResponse
from typing import Callable, Optional
from starlette.types import ASGIApp, ASGIInstance, Scope


def json_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"error": exc.__class__.__name__, "detail": getattr(exc, 'detail', str(exc))}, status_code=getattr(exc, 'status_code', 500))


class AuthenticationFailed(HTTPException):
    pass


class JWTAuthenticationMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret_key: str,
        prefix: str = 'JWT',
        exception_handler: Optional[Callable] = None
    ) -> None:
        self.app = app
        self.secret_key = secret_key
        self.prefix = prefix
        self.exception_handler = exception_handler or json_exception_handler

    def get_token_from_header(self, authorization: str):
        """
        Parses the Authorization header and returns only the token

        :param authorization:
        :return:
        """
        if authorization is None:
            raise AuthenticationFailed(status_code=401, detail='Authorization header is missing')
        try:
            scheme, token = authorization.split()
        except ValueError:
            raise AuthenticationFailed(status_code=401, detail='Could not separate Authorization scheme and token')
        if scheme.lower() != self.prefix.lower():
            raise AuthenticationFailed(status_code=401, detail='Authorization scheme {} is not supported'.format(scheme))
        return token

    def __call__(self, scope: Scope) -> ASGIInstance:
        if scope["type"] in ("http", "websocket"):
            headers = Headers(scope=scope)
            if headers.get('authorization'):
                try:
                    token = self.get_token_from_header(headers.get('authorization'))
                    payload = jwt.decode(token, key=self.secret_key)
                    scope['session'] = payload
                except (AuthenticationFailed, jwt.InvalidTokenError) as e:
                    return self.exception_handler(Request(scope), e)
            else:
                scope['session'] = None

        return self.app(scope)  # pragma: no cover
