from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from routers import article, blog_get, blog_post, file, products, user
from db import models
from db.database import engine
from exceptions import StoryException
from auth import authentication
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(products.router)
app.include_router(file.router)


@app.get("/hello")
def index():
    return "Hello, World!"


@app.exception_handler(StoryException)
async def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.message})


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(bind=engine)

app.mount("/files", StaticFiles(directory="files"), name="files")
