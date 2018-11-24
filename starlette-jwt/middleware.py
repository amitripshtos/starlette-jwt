from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.exceptions import HTTPException
import jwt
from starlette.responses import JSONResponse
from typing import Callable, Optional


def json_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"error": exc.__class__.__name__, "detail": getattr(exc, 'detail', str(exc))}, status_code=getattr(exc, 'status_code', 500))


class AuthenticationFailed(HTTPException):
    pass


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Starlette, secret_key: str, prefix: str='JWT', exception_handler: Optional[Callable]=None):
        super().__init__(app=app)
        self.secret_key = secret_key
        self.prefix = prefix
        self.exception_handler = exception_handler or json_exception_handler

    def get_token_from_header(self, authorization: str):
        if authorization is None:
            raise AuthenticationFailed(status_code=401, detail='Authorization header is missing.')
        try:
            scheme, token = authorization.split()
        except ValueError:
            raise AuthenticationFailed(status_code=401, detail='Could not separate Authorization scheme and token.')
        if scheme.lower() != self.prefix:
            raise AuthenticationFailed(status_code=401, detail='Authorization scheme {} is not supported'.format(scheme))
        return token

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            token = self.get_token_from_header(request.headers.get('authorization'))
            payload = jwt.decode(token, key=self.secret_key)
            request._scope['session'] = payload
            response: StreamingResponse = await call_next(request)
        except (AuthenticationFailed, jwt.InvalidTokenError) as e:
            return self.exception_handler(request, e)

        return response
