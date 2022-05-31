from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db

router = APIRouter(
    prefix="/posts"
)

#create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
#sql create posts code
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    #new_post =  cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#see a post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,  db: Session = Depends(get_db)):
#sql get post code
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
#check if post is not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    return post

#delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
#sql delete a post code
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
#check if deleted and display error
    if post.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail= f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
#updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
#sql update post code
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", 
    #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
#check if there are post with that number
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail= f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()