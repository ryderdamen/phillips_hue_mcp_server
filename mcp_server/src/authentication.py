import json
import requests
import base64
from fastapi import Request, HTTPException
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt


GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUER = "https://accounts.google.com"
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']


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

def verify_google_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth.split(" ")[1]
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]

        jwks = get_jwks()
        jwk = next((key for key in jwks if key["kid"] == kid), None)
        if not jwk:
            raise HTTPException(status_code=403, detail="Public key not found")

        public_key = construct_public_key(jwk)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=GOOGLE_CLIENT_ID,
            issuer=GOOGLE_ISSUER
        )

        if payload.get("email") not in ALLOWED_EMAILS:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid email")

        return payload
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Token verification failed: {str(e)}")
