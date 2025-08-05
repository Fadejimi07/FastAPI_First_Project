from sqlalchemy.orm import Session
from db.models import DbUser
from schemas import UserBase
from db.hash import Hash
from fastapi import HTTPException


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


def update_user(db: Session, user_id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == user_id)
    if user:
        user.update(
            {
                "username": request.username,
                "email": request.email,
                "password": Hash.bcrypt(request.password),
            }
        )
        db.commit()
        db.refresh(user.first())
        return user.first()
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


def delete_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id)
    if user.first():
        user.delete(synchronize_session=False)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user:
        return user
    raise HTTPException(
        status_code=404, detail=f"User with username {username} not found"
    )
