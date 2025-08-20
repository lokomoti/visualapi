"""Signed URL module."""

import time

from auth import jwt
from config import settings

AUDIENCE = "signedurlvisualapi"


class SignedUrlError(Exception):
    """Custom exception for signed URL errors."""


class SignedUrlResourceError(SignedUrlError):
    """Custom exception for signed URL resource errors."""


def create_signed_url(resource: str) -> str:
    """Create a signed URL for a given resource."""
    payload = {
        "resource": resource,
        "exp": int(time.time()) + settings.SIGNED_URL_EXPIRE_SECONDS,
        "aud": AUDIENCE,
    }
    token = jwt.encode_jwt(payload, settings.SIGNED_URL_JWT_SECRET)
    return f"{settings.API_BASE_URL}/signed?token={token}"


def verify_signed_url(token: str, resource: str) -> None:
    """Verify a signed URL."""
    try:
        payload = jwt.decode_jwt(
            secret=settings.SIGNED_URL_JWT_SECRET, token=token, audience=AUDIENCE
        )
    except jwt.JWTExpiredError:
        raise SignedUrlError("Token has expired")
    
    except jwt.JWTDecodeError as e:
        raise SignedUrlError("Invalid token")

    if not payload.get("resource") == resource:
        raise SignedUrlResourceError("Invalid resource")

    if not payload.get("aud") == AUDIENCE:
        raise SignedUrlError("Invalid audience")
