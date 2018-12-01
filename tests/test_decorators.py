from starlette.applications import Starlette
from starlette_jwt import JWTAuthenticationMiddleware, anonymous_allowed, authentication_required
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
import jwt


@authentication_required
async def with_auth(request, *args, **kwargs):
    return JSONResponse({'session': {"username": request.session.get('username')}})


@anonymous_allowed
async def without_auth(request):
    return JSONResponse({'session': None})


def create_app():
    app = Starlette()
    app.add_route("/auth", with_auth, methods=["GET"])
    app.add_route("/no-auth", without_auth, methods=["GET"])
    return app


def test_decorators():
    secret_key = 'example'
    app = create_app()
    app.add_middleware(JWTAuthenticationMiddleware, secret_key=secret_key, prefix='JWT')
    client = TestClient(app)

    response = client.get("/auth")
    assert response.status_code == 401
    assert response.text == 'Authentication credentials were not provided'

    response = client.get("/auth", headers=dict(Authorization=f'JWT {jwt.encode(dict(username="user"), secret_key).decode()}'))
    assert response.json() == {"session": {"username": "user"}}

    response = client.get("/no-auth")
    assert response.json() == {'session': None}
