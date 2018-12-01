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
from starlette_jwt import JWTAuthenticationMiddleware, authentication_required, anonymous_allowed


app = Starlette()
app.add_middleware(JWTAuthenticationMiddleware, secret_key='secret', prefix='JWT')
```

Access the JWT payload in a request,
Enforce handlers to be with authentication.

The `@authentication_required` decorator will enforce the user to be logged in for that route. Meanwhile the `@anonymous_allowed` will allow anonymous users to hit the route. 

The default behavior is `@anonymous_allowed` so your code be explicit.

```python
def my_handler(request):
@app.route('/noauth')
@authentication_required
async def homepage(request):
    return JSONResponse({'payload': request.session})
```

Not all handlers must be with authentication
```python
@app.route('/noauth')
@anonymous_allowed
async def homepage(request):
    return JSONResponse({'payload': None})
```

## Settings

*secret_key*

Store your secret key in this setting while creating the middleware:
```python
app.add_middleware(JWTAuthenticationMiddleware, secret_key='MY SECRET KEY')
```

*prefix*

Change the Authorization header prefix string (defualts to "JWT"):
```python
# Example: changes the prefix to Bearer
app.add_middleware(JWTAuthenticationMiddleware, secret_key='secret', prefix='Bearer')
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

## Thanks
*  Starlette project - https://github.com/encode/starlette
* apistar-jwt project - https://github.com/audiolion/apistar-jwt