from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

@router.get(
        '/all',
        response_description="List of available blogs")
def get_all_blogs(page = 1, page_size: Optional[int] = None):
    return {"message": f"All {page_size} blogs on {page}"}

@router.get("/{id}/comments/{comment_id}", tags=['comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {"message": f"blog_id {id}, comment_id: {comment_id}, valid: {valid}, username: {username}"}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howTo = 'howTo'

@router.get("/type/{type}", 
         summary="Information about type of a blog")
def get_blog_type(type: BlogType):
    """
    Simulates retrieving types of blogs 
    
    - **type** mandatory type of the blog
    """
    return {"message": f"Blog type: {type}"}

@router.get("/{id}")
def get_blog(id: int, response: Response):
    if (id > 5):
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'error': f'Blog {id} not found'}
    else:
        response.status_code=status.HTTP_200_OK
        return {"message": f"Hello, World! {id}"}
