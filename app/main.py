from os import curdir
from turtle import title
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print('Error: ', error)
        time.sleep(2)


my_posts = [{"title": "post1", "content": "content1", "id": 1}, {"title": "post2", "content": "content2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)): 
    # with regular sql
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()   
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# this validate the payload based on the pydentic validator
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):   
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title = post.title, content=post.content, published=post.published)
    # so instead of distructure post one after the other you can just do the following bellow **post.dict()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # this returns back the post
    db.refresh(new_post)
    return new_post
    

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):    
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if  not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # delete_post = cursor.fetchone()

    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    # this deletes the post if it exists
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""", (post.title, post.content, post.published, str(id)))
    # conn.commit()
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    # this returns back the post
    db.refresh(new_user)
    return new_user