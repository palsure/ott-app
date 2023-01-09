#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ

#----------------------------------------------------------------------------#
# auth setup
#----------------------------------------------------------------------------#

AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN', 'sure-ott.us.auth0.com')
ALGORITHMS = environ.get('ALGORITHMS', ['RS256'])
API_AUDIENCE = environ.get('API_AUDIENCE', 'sure-ott')

#----------------------------------------------------------------------------#
# AuthError Exception
#----------------------------------------------------------------------------#
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


#----------------------------------------------------------------------------#
# Auth Header
#----------------------------------------------------------------------------#
'''
Auth Header
    get's the Authorization header from the request
    validates the Authorization is in correct format
    throws an AuthError for missing or invalid Authorization header
    return the token part of the header
'''


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is required"
            }, 401
        )

    header_parts = auth_header.split(' ')

    if (not header_parts or len(header_parts) !=
            2 or header_parts[0].lower() != "bearer"):
        raise AuthError(
            {
                "code": "authorization_header_invalid",
                "description": "Authorization header must be in the 'Bearer token' format"},
            401)

    return header_parts[1]


#----------------------------------------------------------------------------#
# Check Permissions
#----------------------------------------------------------------------------#
'''
Check Permissions
    Check's the permissions in the request has the allowed permission for the endpoint
    validates the Authorization is in correct format
    thows an AuthError if permissions are not included in the payload or
        the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError(
            {
                "code": "permission_missing",
                "description": "Permission is missing in payload"
            }, 403)

    if permission not in payload['permissions']:
        raise AuthError(
            {
                "code": "permission_invalid",
                "description": "Permission is invalid/not allowed"
            }, 403)


#----------------------------------------------------------------------------#
# Verify decoded JWT
#----------------------------------------------------------------------------#
'''
Verify decoded JWT
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "header_invalid",
                "description": "Authorization malformed"
            }, 401
        )

    rsa_key = {}

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


#----------------------------------------------------------------------------#
# Auth Decorator
#----------------------------------------------------------------------------#
'''
Auth Decorator
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                print(sys.exc_info())
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Access denied due to invalid token'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
