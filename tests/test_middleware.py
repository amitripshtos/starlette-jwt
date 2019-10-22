import pytest
from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect, WebSocket

from starlette_jwt import JWTAuthenticationBackend, JWTUser
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette.middleware.authentication import AuthenticationMiddleware
import jwt
from starlette.authentication import requires
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os


@requires('authenticated')
async def with_auth(request):
    return JSONResponse({'auth': {"username": request.user.display_name}})


async def without_auth(request):
    return JSONResponse({'auth': None})


async def ws_without_auth(websocket):
    websocket = WebSocket(scope=websocket.scope, receive=websocket.receive, send=websocket.send)
    await websocket.accept()
    await websocket.send_text('No Authentication')
    await websocket.close()


@requires('authenticated')
async def ws_with_auth(websocket):
    websocket = WebSocket(scope=websocket.scope, receive=websocket.receive, send=websocket.send)
    await websocket.accept()
    await websocket.send_text('Authentication valid')
    await websocket.close()


def create_app():
    app = Starlette()
    app.add_route("/auth", with_auth, methods=["GET"])
    app.add_route("/no-auth", without_auth, methods=["GET"])
    app.add_websocket_route("/ws-auth", ws_with_auth)
    app.add_websocket_route("/ws-no-auth", ws_without_auth)
    return app


def test_websocket_pass_authentication_without_headers():
    app = create_app()
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='example'))
    client = TestClient(app)
    with client.websocket_connect("/ws-no-auth") as websocket:
        data = websocket.receive_text()
        assert data == 'No Authentication'


@pytest.mark.xfail(raises=WebSocketDisconnect)
def test_websocket_fail_authentication_without_headers():
    app = create_app()
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='example'))
    client = TestClient(app)
    with client.websocket_connect("/ws-auth") as websocket:
        pass


def test_websocket_valid_authentication():
    secret_key = 'example'
    app = create_app()
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=secret_key))
    client = TestClient(app)
    token = jwt.encode(dict(username="user"), secret_key, algorithm="HS256").decode()
    with client.websocket_connect("/ws-auth", headers=dict(Authorization=f'JWT {token}')) as websocket:
        data = websocket.receive_text()
        assert data == 'Authentication valid'
        assert websocket.scope['user'].is_authenticated


def test_header_parse():
    secret_key = 'example'
    app = create_app()
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=secret_key))
    client = TestClient(app)

    # No token for auth endpoint
    response = client.get("/auth")
    assert response.text == 'Forbidden'
    assert response.status_code == 403

    # Without prefix
    response = client.get("/auth",
                          headers=dict(Authorization=jwt.encode(dict(username="user"), secret_key, algorithm='HS256').decode()))
    assert response.text == 'Could not separate Authorization scheme and token'
    assert response.status_code == 400

    # Wrong prefix
    response = client.get("/auth",
                          headers=dict(Authorization=f'WRONG {jwt.encode(dict(username="user"), secret_key, algorithm="HS256").decode()}'))
    assert response.text == 'Authorization scheme WRONG is not supported'
    assert response.status_code == 400

    # Good headers
    response = client.get("/auth", headers=dict(Authorization=f'JWT {jwt.encode(dict(username="user"), secret_key, algorithm="HS256").decode()}'))
    assert response.json() == {"auth": {"username": "user"}}
    assert response.status_code == 200

    # Wrong secret key
    response = client.get("/auth",
                          headers=dict(Authorization=f'JWT {jwt.encode(dict(username="user"), "BAD SECRET", algorithm="HS256").decode()}'))
    assert response.text == 'Signature verification failed'
    assert response.status_code == 400


def test_get_token_from_header():
    token = jwt.encode(dict(username="user"), 'secret', algorithm="HS256").decode()
    assert token == JWTAuthenticationBackend.get_token_from_header(authorization=f'JWT {token}', prefix='JWT')


def test_user_object():
    payload = dict(username="user")
    token = jwt.encode(payload, "BAD SECRET", algorithm="HS256").decode()
    user_object = JWTUser(username="user", payload=payload, token=token)
    assert user_object.is_authenticated == True
    assert user_object.display_name == 'user'
    assert user_object.token == token
    assert user_object.payload == payload


def test_endpoint_without_authentication():
    """
    This test makes sure that we are able to have endpoints without any authentication.
    """
    secret_key = 'example'
    app = create_app()
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=secret_key, algorithm='RS256'))
    client = TestClient(app)
    response = client.get("/no-auth")
    assert response.text == '{"auth":null}'
    assert response.status_code == 200


def test_rsa_algorithm():
    """
    This test makes sure RSA algo works with starlette-jwt
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir,"./test-key.pem"), "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with open(os.path.join(current_dir, "test-key.pub"), "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    app = create_app()
    app.add_middleware(AuthenticationMiddleware,
                       backend=JWTAuthenticationBackend(secret_key=public_key, algorithm='RS256'))
    client = TestClient(app)
    response = client.get("/auth",
                          headers=dict(
                              Authorization=f'JWT {jwt.encode(dict(username="user"), private_key, algorithm="RS256").decode()}'))
    assert response.json() == {"auth":{"username":"user"}}
    assert response.status_code == 200
