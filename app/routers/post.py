from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import engine, get_db

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)): 
    # with regular sql
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()   
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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
    

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):    
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if  not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.Post)
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