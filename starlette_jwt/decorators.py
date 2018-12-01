from starlette_jwt import AuthenticationFailed
import functools


def authentication_required(func):
    """
    Wrapper around a method (handler) that will check if the session data and the header exist and will raise an exception in case they won't.

    :param func:
    :return:
    """
    @functools.wraps(func)
    async def wrapper_verify_authentication(request, *args, **kwargs):
        if 'authorization' not in request.headers or not request.session:
            raise AuthenticationFailed(status_code=401, detail='Authentication credentials were not provided')

        return await func(request, *args, **kwargs)

    return wrapper_verify_authentication


def anonymous_allowed(fn):
    return fn
