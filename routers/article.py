import token
from typing import List
from schemas import ArticleBase, ArticleDisplay, UserBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_article
from auth.oauth2 import (
    get_current_user,
    oauth2_schema,
)  # Make sure this import path matches your project structure

router = APIRouter(prefix="/article", tags=["article"])


# Create article
@router.post("/", response_model=ArticleDisplay)
def create_article(
    request: ArticleBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    article = db_article.create_article(db, request)
    db.refresh(article)
    return article


# Get article
@router.get("/{article_id}")
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    """article = db_article.get_article(db, article_id)
    if article is None:
        return {"error": "Article not found"}
    return article"""
    return {
        "data": db_article.get_article(db, article_id),
        "current_user": current_user,
    }
