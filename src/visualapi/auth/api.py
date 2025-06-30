import os

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import blacklist as jwt_blacklist
from auth.jwt import JWTDecodeError, JWTExpiredError, decode_jwt

# JWT audience for the Visual API
AUDIENCE = "visualapi"


def authorize(token: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> None:
    """Authorize a request by decoding the JWT token.

    Args:
        token: The HTTPAuthorizationCredentials containing the JWT token.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    try:
        payload = decode_jwt(token.credentials, audience=AUDIENCE)
        jti = payload.get("jti")

        if not jti:
            raise HTTPException(status_code=401, detail="Token missing jti")

        if jwt_blacklist.is_token_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token is blacklisted")

    except JWTExpiredError:
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTDecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
