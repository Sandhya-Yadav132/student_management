from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, BlacklistedToken
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session, user_data: UserCreate) -> User:
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return create_access_token(data={"sub": user.username})

def logout_user(db: Session, token: str) -> dict:
    db.add(BlacklistedToken(token=token))
    db.commit()
    return {"message": "Successfully logged out"}
