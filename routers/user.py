from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay
from typing import List

router = APIRouter(prefix="/user", tags=["user"])


# Create user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return db_user.get_all_users(db)


# Read user
@router.get("/{user_id}", response_model=UserDisplay)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    user = db_user.get_user(db, user_id)
    if user is None:
        return {"error": "User not found"}
    return user


# Update user
@router.put("/{user_id}")
def update_user(
    user_id: int,
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    user = db_user.update_user(db, user_id, request)
    if user is None:
        return {"error": "User not found"}
    return {"message": "User updated successfully", "user": user}


# Delete user
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    response = db_user.delete_user(db, user_id)
    return response
