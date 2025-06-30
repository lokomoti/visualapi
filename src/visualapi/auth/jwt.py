"""JWT authentication utilities for the Visual API."""

import os

import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("API_JWT_SECRET")
JWT_ALGORITHM = os.getenv("API_JWT_ALGORITHM", "HS256")


class JWTDecodeError(Exception):
    """Exception raised for errors in decoding JWT tokens."""

    pass


class JWTExpiredError(JWTDecodeError):
    """Exception raised when a JWT token has expired."""

    pass


def decode_jwt(token: str, audience: str) -> dict:
    """Decode a JWT token and return the payload.
    Args:
        token (str): The JWT token to decode.
        audience (str): The expected audience of the token.
    Returns:
        dict: The decoded payload of the JWT token.
    Raises:
        JWTDecodeError: If the token is invalid or cannot be decoded.
        JWTExpiredError: If the token has expired.
    """
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=audience
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTExpiredError("Token expired")
    except jwt.InvalidTokenError:
        raise JWTDecodeError("Invalid token")


def encode_jwt(payload: dict) -> str:
    """Encode a payload into a JWT token.
    Args:
        payload (dict): The payload to encode into a JWT token.
    Returns:
        str: The encoded JWT token.
    """
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
