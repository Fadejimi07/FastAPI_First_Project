from db.models import DbArticle
from schemas import ArticleBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from exceptions import StoryException


def create_article(db: Session, request: ArticleBase):
    if request.content.startswith("Once upon a time"):
        raise StoryException(
            name="StoryException", message="Once upon a time stories are not allowed."
        )
    try:
        new_article = DbArticle(
            title=request.title,
            content=request.content,
            published=request.published,
            user_id=request.creator_id,
        )

        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Article creation failed due to integrity error"
        )


def get_article(db: Session, article_id: int):
    article = db.query(DbArticle).filter(DbArticle.id == article_id).first()
    if article:
        return article
    raise HTTPException(
        status_code=404, detail=f"Article with id {article_id} not found"
    )
