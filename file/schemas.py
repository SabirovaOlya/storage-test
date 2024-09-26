from pydantic import BaseModel, FilePath


class CreateFile(BaseModel):
    team_id: str
    project_name: str
    file_path: str
    