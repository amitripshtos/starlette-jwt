from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
from starlette_jwt import JWTAuthenticationBackend
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware

app = Starlette()
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key='secret', prefix='JWT'))


@app.route('/noauth')
async def homepage(request):
    return JSONResponse({'hello': 'world'})


@app.route('/auth')
@requires('authenticated')
async def homepage(request):
    return JSONResponse({'hello': request.session['username']})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
