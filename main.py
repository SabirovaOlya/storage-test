import os
import uvicorn
import zipfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from core.models import Base, db_helper
from file.views import router as file_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(file_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
