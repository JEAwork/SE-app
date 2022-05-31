from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from requests import post
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from . database import engine, get_db
from . routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Tryconnection hardcoded login
while True:
    try:
        conn = psycopg2.connect(host='localhost', database ='fastapi', user ='postgres', 
        password='zxxznmmn', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected!")
        break

    except Exception as error:
        print("Connection Failed")
        print("Error: ", error)
        time.sleep(2)

#temporary data
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title:" :
"favorite foods", "content": "I like pizza", "id": 2}]

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#finding posts
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

app.include_router(post.router)
app.include_router(user.router)


#get request method url: "/"
@app.get("/")
def root():
    return {"message": "Testing"}

#get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
#sql get all posts code
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


#Pathways
#venv\Scripts\activate.bat 
#uvicorn app.main:app --reload
