from sqlalchemy.ext.asyncio import AsyncSession
from file.schemas import CreateFile
from core.models import File


async def create_file(session: AsyncSession, data: dict):
    new_file = File(**data.dict())
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file
