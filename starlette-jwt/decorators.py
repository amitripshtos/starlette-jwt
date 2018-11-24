
def anonymous_allowed(fn):
    fn.authenticated = False
    return fn


def authentication_required(fn):
    fn.authenticated = True
    return fn