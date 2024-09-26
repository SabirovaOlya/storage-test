from typing import Annotated

from fastapi import APIRouter, Path
from schemas import CreateFile
import crud

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
def file_upload(file: CreateFile):
    return crud.create_file(data=file)

