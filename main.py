from fastapi import FastAPI
from database.database import engine
from typing import List
import uvicorn

from models import models
from schemas import schemas
from routes import course, student, users, loginauth

app = FastAPI()

# Create table on database
models.Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(loginauth.router)
app.include_router(student.router)
app.include_router(course.router)

if __name__ == '__main__':
    uvicorn.run('main.app', host = '0.0.0.0', port = 8000, reload = True)