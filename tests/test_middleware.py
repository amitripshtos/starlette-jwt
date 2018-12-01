from starlette.applications import Starlette
from starlette_jwt import JWTAuthenticationMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
import jwt


async def with_auth(request):
    return JSONResponse({'session': {"username": request.session.get('username')}})


async def without_auth(request):
    return JSONResponse({'session': None})


def create_app():
    app = Starlette()
    app.add_route("/auth", with_auth, methods=["GET"])
    app.add_route("/no-auth", without_auth, methods=["GET"])
    return app


def test_header_parse():
    secret_key = 'example'
    app = create_app()
    app.add_middleware(JWTAuthenticationMiddleware, secret_key=secret_key, prefix='JWT')
    client = TestClient(app)

    # Without prefix
    response = client.get("/auth",
                          headers=dict(Authorization=jwt.encode(dict(username="user"), secret_key).decode()))
    assert response.json() == {'detail': 'Could not separate Authorization scheme and token', 'error': 'AuthenticationFailed'}

    # Wrong prefix
    response = client.get("/auth",
                          headers=dict(Authorization=f'WRONG {jwt.encode(dict(username="user"), secret_key).decode()}'))
    assert response.json() == {'detail': 'Authorization scheme WRONG is not supported', 'error': 'AuthenticationFailed'}

    # Good headers
    response = client.get("/auth", headers=dict(Authorization=f'JWT {jwt.encode(dict(username="user"), secret_key).decode()}'))
    assert response.json() == {"session": {"username": "user"}}
