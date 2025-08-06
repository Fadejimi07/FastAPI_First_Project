from custom_log import log
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi import BackgroundTasks

from schemas import ProductBase

router = APIRouter(prefix="/template", tags=["Template"])

templates = Jinja2Templates(directory="templates")


@router.post("/products/{id}", response_class=HTMLResponse)
def get_product(id: str, product: ProductBase, request: Request, bt: BackgroundTasks):
    bt.add_task(log_template_call, f"Product {id} requested with data: {product}")
    return templates.TemplateResponse(
        "product.html", {"request": request, "id": id, "product": product}
    )


def log_template_call(message: str):
    log("MyAPI", message)
