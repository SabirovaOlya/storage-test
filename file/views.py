from fastapi import APIRouter
from schemas import CreateFile
from file import crud

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
def file_upload(file: CreateFile):
    return crud.create_file(data=file)

