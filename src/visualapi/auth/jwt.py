"""JWT authentication utilities for the Visual API."""

import jwt

JWT_ALGORITHM = "HS256"


class JWTDecodeError(Exception):
    """Exception raised for errors in decoding JWT tokens."""

    pass


class JWTExpiredError(JWTDecodeError):
    """Exception raised when a JWT token has expired."""

    pass


def decode_jwt(secret: str, token: str, audience: str) -> dict:
    """Decode a JWT token and return the payload.
    Args:
        secret: The secret key used to decode the token.
        token: The JWT token to decode.
        audience: The expected audience of the token.
    Returns:
        The decoded payload of the JWT token.
    Raises:
        JWTDecodeError: If the token is invalid or cannot be decoded.
        JWTExpiredError: If the token has expired.
    """
    try:
        payload = jwt.decode(
            token, secret, algorithms=[JWT_ALGORITHM], audience=audience
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise JWTExpiredError("Token expired")

    except jwt.InvalidTokenError:
        raise JWTDecodeError("Invalid token")


def encode_jwt(payload: dict, secret: str) -> str:
    """Encode a payload into a JWT token.
    Args:
        payload: The payload to encode into a JWT token.
        secret: The secret key used to encode the token.
    Returns:
        The encoded JWT token.
    """
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
