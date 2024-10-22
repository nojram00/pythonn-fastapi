import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Header, Request, Response
from functools import wraps
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key_code')
ALGORITHM = os.environ.get('ALG', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict, expires : Optional[timedelta] = None) -> str:
    encoded = data.copy()

    if expires:
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded.update({"exp" : expire})
    return jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token : str) -> dict :
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


def Auth(func):
    @wraps(func)
    async def wrapper(request : Request, *args, **kwargs):

        authorization = request.headers.get("authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header is missing")
        
        scheme, _ , token = authorization.partition(" ")

        if scheme.lower() != 'bearer' or not token:
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    
        payload = verify_token(token)

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return func(payload, *args, **kwargs)
    
    return wrapper