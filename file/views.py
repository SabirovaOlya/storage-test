import os
import zipfile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from file import crud
from core.models import db_helper
from file.schemas import CreateFile

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def file_upload(
    session: AsyncSession = Depends(db_helper.session_dependency),
    file: UploadFile = File(...),
    project_name: str = Form(...),
    team_id: str = Form(...),
):

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")

    storage_dir = os.path.join("storage", team_id, project_name)
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
        print(f"Directory created: {storage_dir}")

    absolute_file_path = os.path.abspath(storage_dir)
    zip_file_path = os.path.join(storage_dir, file.filename.replace(" ", "-"))
    try:
        with open(zip_file_path, 'wb+') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(absolute_file_path)

    except Exception as e:
        return {"message": f"There was an error processing the file: {str(e)}"}
    finally:
        file.file.close()
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)

    file_data = CreateFile(team_id=team_id, project_name=project_name, file_path=absolute_file_path)
    return await crud.create_file(session=session, data=file_data)

    # return {
    #     "message": f"Successfully uploaded and extracted {file.filename} to {team_id}/{project_name}",
    #     "extracted_to": absolute_file_path
    # }
    # return crud.create_file(data=file)

