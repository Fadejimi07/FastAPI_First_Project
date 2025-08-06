from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from routers import article, blog_get, blog_post, file, products, user, dependency
from db import models
from db.database import engine
from exceptions import StoryException
from auth import authentication
from fastapi.staticfiles import StaticFiles
from templates import templates
import time

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(products.router)
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(dependency.router)


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


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["duration"] = str(process_time)
    return response


app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")
