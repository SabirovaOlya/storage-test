from core.models.base import Base
from sqlalchemy.orm import Mapped


class File(Base):
    __tablename__ = "files"

    team_id: Mapped[str]
    project_name: Mapped[str]
    file_path: Mapped[str]