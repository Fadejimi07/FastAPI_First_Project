from typing import Optional, List
from fastapi import APIRouter, Cookie, Form, Header
from fastapi.responses import PlainTextResponse, Response, HTMLResponse

router = APIRouter(prefix="/product", tags=["Product"])

products = ["watch", "phone", "laptop"]


@router.post("/new")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/all")
def get_all_products():
    # return products
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="cookie_value")
    return response


@router.get("/withheader")
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    response.headers["custom_response_header"] = (
        ", ".join(custom_header) if custom_header else "No custom header"
    )
    return {
        "data": products,
        "custom_header": custom_header,
        "test_cookie": test_cookie,
    }


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Returns the html for an object",
        },
        404: {
            "content": {"text/plain": {"example": "Product not found"}},
            "description": "A clear text error message when the product is not found",
        },
    },
)
def get_product(id: int):
    if id >= len(products) or id < 0:
        return PlainTextResponse(
            content="Product not found", media_type="text/plain", status_code=404
        )
    prodcut = products[id]
    out = f"""
    <head>
        <style>
            .product {{
                width: 500px;
                height: 500px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
                padding: 20px;
            }}
        </style>
    </head>
    <div class="product">Random Product: {prodcut}</div>
    """
    return HTMLResponse(content=out, media_type="text/html")
