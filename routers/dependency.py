from fastapi import APIRouter, Depends
from fastapi.requests import Request

router = APIRouter(prefix="/dependency", tags=["Dependency Injection"])


def convert_headers(request: Request):
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} -- {value}")
    return out_headers


@router.get("")
def get_items(headers=Depends(convert_headers)):
    return {"headers": headers}
