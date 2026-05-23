import requests
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
_jwks: dict | None = None


def get_jwks() -> dict:
    global _jwks
    if _jwks is None:
        _jwks = requests.get(settings.keycloak_jwks_url).json()
    return _jwks


def get_jwk(kid: str) -> dict:
    for key in get_jwks()["keys"]:
        if key["kid"] == kid:
            return key
    raise HTTPException(status_code=401, detail="Invalid token key")


def decode_jwt(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        jwk = get_jwk(header["kid"])
        return jwt.decode(
            token,
            jwk,
            algorithms=["RS256"],
            audience=settings.keycloak_client_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(exc)}")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_jwt(token)
