from jose import jwt, JWTError
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import UserModel
from database import get_db
import os

# Use an environment variable for the secret key
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Hash password
def hash_password(password: str) -> str:
    return ph.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False

# Create access token (JWT)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add expiration
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")  # Extract user_id from the payload
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")  # Log the error
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()  # Query by user_id
    if user is None:
        raise credentials_exception
    return user
