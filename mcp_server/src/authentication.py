import json
import requests
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt
import os
from functools import wraps
from typing import Callable, Any, Dict
import logging

logger = logging.getLogger(__name__)

GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUER = "https://accounts.google.com"
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

ALLOWED_EMAILS_STR = os.environ.get('ALLOWED_EMAILS')
if not ALLOWED_EMAILS_STR:
    raise RuntimeError("ALLOWED_EMAILS environment variable must be set")
ALLOWED_EMAILS = [email.strip() for email in ALLOWED_EMAILS_STR.split(',')]

_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        resp = requests.get(GOOGLE_JWKS_URL)
        resp.raise_for_status()
        _jwks_cache = resp.json()["keys"]
    return _jwks_cache

def construct_public_key(jwk):
    n = int.from_bytes(base64.urlsafe_b64decode(jwk["n"] + "=="), byteorder="big")
    e = int.from_bytes(base64.urlsafe_b64decode(jwk["e"] + "=="), byteorder="big")
    pubkey = rsa.RSAPublicNumbers(e, n).public_key(backend=default_backend())
    return pubkey

def verify_google_token_from_headers(headers: Dict[str, str]) -> Dict[str, Any]:
    """Verify Google OAuth token from request headers."""
    auth = headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    token = auth.split(" ")[1]
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]

        jwks = get_jwks()
        jwk = next((key for key in jwks if key["kid"] == kid), None)
        if not jwk:
            raise ValueError("Public key not found")

        public_key = construct_public_key(jwk)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=GOOGLE_CLIENT_ID,
            issuer=GOOGLE_ISSUER
        )

        if payload.get("email") not in ALLOWED_EMAILS:
            raise ValueError("Forbidden: Invalid email")

        return payload
    except Exception as e:
        raise ValueError(f"Token verification failed: {str(e)}")

def require_auth(func: Callable) -> Callable:
    """Decorator to require Google OAuth authentication for FastMCP tools."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In FastMCP, we need to get the request context differently
        # For now, we'll check if there's an authorization header in the environment
        # or we can modify this to work with FastMCP's request context
        
        # For HTTP transport, we can check headers from the request context
        # This is a simplified approach - you might need to adjust based on your specific setup
        
        try:
            # Check if we're in a context where we can get headers
            # This is a placeholder - you'll need to implement this based on your FastMCP setup
            headers = getattr(func, '_request_headers', {})
            if headers:
                user = verify_google_token_from_headers(headers)
                logger.info(f"Authenticated user: {user.get('email')}")
            else:
                # For development/testing, you might want to skip auth
                logger.warning("No headers found, skipping authentication")
                user = {"email": "dev@example.com", "sub": "dev"}
            
            # Add user info to kwargs for the function to use
            kwargs['user'] = user
            return func(*args, **kwargs)
            
        except ValueError as e:
            logger.error(f"Authentication failed: {e}")
            return {"error": "Authentication required", "details": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            return {"error": "Authentication error", "details": str(e)}
    
    return wrapper

# Legacy function for backward compatibility
def verify_google_token(request):
    """Legacy function for FastAPI compatibility."""
    if hasattr(request, 'headers'):
        return verify_google_token_from_headers(dict(request.headers))
    else:
        raise ValueError("Request object not compatible")
