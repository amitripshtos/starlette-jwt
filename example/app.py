from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
from starlette_jwt import JWTAuthenticationMiddleware, authentication_required, anonymous_allowed


app = Starlette()
app.add_middleware(JWTAuthenticationMiddleware, secret_key='secret', prefix='JWT')


@app.route('/noauth')
@anonymous_allowed
async def homepage(request):
    return JSONResponse({'hello': 'world'})


@app.route('/auth')
@authentication_required
async def homepage(request):
    return JSONResponse({'hello': request.session['username']})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
