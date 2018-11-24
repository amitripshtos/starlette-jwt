from .middleware import JWTAuthenticationMiddleware,AuthenticationFailed

__author__ = """Ryan Castner"""
__email__ = 'castner.rr@gmail.com'
__version__ = '0.5.0'

__all__ = ['JWTAuthenticationMiddleware', 'AuthenticationFailed', 'anonymous_allowed', 'authentication_required']