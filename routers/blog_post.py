from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    number_of_comment: int = 0
    tags: List[str] = []
    metadata: Dict[str, str] = {"key1": "value1", "key2": "value2"}
    image: Optional[Image] = None


@router.post("/new/{id}")
def create_blog(id: int, blog: BlogModel, version: int = 1):
    return {"data": blog, "id": id, "version": version}


@router.post("/new/{id}/comment")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: str = Query(
        None,
        title="Title of the comment",
        description="Some description of the comment",
        alias="commentTitle",
    ),
    comment_id: int = Path(gt=5, le=10),
    content: str = Body(..., min_length=10, max_length=50, regex=r"^[a-z\s]+$"),
    v: Optional[List[str]] = Query(
        ["1.0", "1.1", "1.2"], title="Version", description="Version of the API"
    ),
):
    return {
        "data": blog,
        "id": id,
        "comment_id": comment_id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
    }
