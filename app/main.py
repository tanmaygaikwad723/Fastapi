from fastapi import FastAPI
from fastapi.params import Body
from  . import models
from .database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="0104", cursor_factory=RealDictCursor)
    cur = connection.cursor()
    print("Database connected")
except Exception as error:
    print(f"Connection to database failed, the error was {error}")

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hey"
    }



