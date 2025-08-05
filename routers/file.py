from fastapi import APIRouter, File, UploadFile
import shutil

from fastapi.responses import FileResponse

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/file")
def get_file(file: bytes = File(...)):
    contents = file.decode("utf-8")
    lines = contents.split("\n")
    return {"lines": lines}


@router.post("/upload-file")
def get_upload_file(file: UploadFile = File(...)):
    path = f"files/{file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": path,
        "type": file.content_type,
    }


@router.get("/download/{name}", response_class=FileResponse)
def get_download_file(name: str):
    path = f"files/{name}"
    return path
