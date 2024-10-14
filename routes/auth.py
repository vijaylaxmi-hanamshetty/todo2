from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from schema import UserCreate, Token
from crud import get_user_by_username, create_user
from database import get_db
from security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    create_user(db, user)
    return {"message": "User registered successfully"}

# Login to obtain token
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    
    # Validate user credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Set the token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create access token, include user_id in the token payload
    access_token = create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)
    
    # Return the access token with the correct structure
    return {"access_token": access_token, "token_type": "bearer"}