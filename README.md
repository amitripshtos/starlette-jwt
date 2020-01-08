# starlette-jwt
JWT Middleware for the pythonic Starlette API framework

# starlette-jwt

[![pypi](https://img.shields.io/pypi/v/starlette_jwt.svg)](https://pypi.org/project/starlette-jwt) [![travis](https://img.shields.io/travis/amitripshtos/starlette-jwt.svg)](https://travis-ci.org/amitripshtos/starlette-jwt) [![codecov](https://codecov.io/gh/amitripshtos/starlette-jwt/branch/master/graph/badge.svg)](https://codecov.io/gh/amitripshtos/starlette-jwt)


JSON Web Token Middleware for use with Starlette framework.

## Installation

```
$ pip install starlette-jwt
```

Alternatively, install through [pipenv](https://pipenv.readthedocs.io/en/latest/).

```
$ pipenv install starlette-jwt
```

## Usage


Register the Middleware with your app.

```python
from starlette.applications import Starlette
from starlette_jwt import JWTAuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware

app = Starlette()
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='secret', prefix='JWT'))

```

Access the JWT payload in a request,
Enforce handlers to be with authentication.

The `@authentication_required` decorator will enforce the user to be logged in for that route. Meanwhile the `@anonymous_allowed` will allow anonymous users to hit the route. 

The default behavior is `@anonymous_allowed` so your code be explicit.

```python
from starlette.authentication import requires

def my_handler(request):
@app.route('/noauth')
@requires('authenticated')
async def homepage(request):
    return JSONResponse({'payload': request.session})
```

Not all handlers must be with authentication
```python
@app.route('/noauth')
async def homepage(request):
    return JSONResponse({'payload': None})
```

## Settings

*secret_key*

Store your secret key in this setting while creating the middleware:
```python
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='MY SECRET KEY'))
```

*algorithm*

Configures the jwt algorithm to use (defaults to "HS256", "RSA256" available):
```python
public_key = b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC...'
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=public_key, algorithm='RS256'))
```

**NOTE:** In order to make starlette-jwt with the RSA256 Algorithm, you must have the package cryptography>=2.7

*prefix*

Change the Authorization header prefix string (defaults to "JWT"):
```python
# Example: changes the prefix to Bearer
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='secret', prefix='Bearer'))
```

*username_field*

The user name field in the JWT token payload:
```python
# Example: changes the username field to "user"
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='secret', username_field='user'))
```

## Todo

*  Support JWT token standard payload
*  Set JWT options (time expiration for example)


## Developing

This project uses [`pipenv`](https://docs.pipenv.org) to manage its development environment, and [`pytest`](https://docs.pytest.org) as its tests runner.  To install development dependencies:

```
pipenv install --dev
```

To run tests:

```
pipenv shell
pytest
```

This project uses [Codecov](https://codecov.io/gh/amitripshtos/starlette-jwt) to enforce code coverage on all pull requests.  To run tests locally and output a code coverage report, run:

```
pipenv shell
pytest --cov=starlette_test/
```

# Deploying new version to pypi (Maintainers)
```bash

python3.7 setup.py sdist
twine upload --repository-url https://pypi.org/legacy/ dist/*

```
## Thanks
*  Starlette project - https://github.com/encode/starlette
* apistar-jwt project - https://github.com/audiolion/apistar-jwt
