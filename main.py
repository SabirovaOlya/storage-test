import os
import uvicorn
import zipfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from file_view import router as file_router
app = FastAPI()
# app.include_router(file_router)


@app.post("/file/upload")
def upload(
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

    return {
        "message": f"Successfully uploaded and extracted {file.filename} to {team_id}/{project_name}",
        "extracted_to": absolute_file_path
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
