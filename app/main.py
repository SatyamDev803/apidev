from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import Post, PostCreate


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    # Connect to your postgres DB
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'apidev', user = 'postgres', password = 'rootuser', cursor_factory = RealDictCursor)
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection established")
        break
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        time.sleep(2)


my_posts = [
    {
        'title': 'Post 1',
        'content': 'Content of post 1',
        'id': 1,
    },
    {
        'title': 'Post 2',
        'content': 'Content of post 2',
        'id': 2,
    },
    {
        'title': 'Post 3',
        'content': 'Content of post 3',
        'id': 3,
    }
]


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def read_root():
    return {"Message": "Welcome to the FastAPI application!"}


@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # Prone to SQL Injection (The user can enter the SQL query directly into the values fields)
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})") 

    # cursor.execute(""" INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post.model_dump()) #Standard way
    # print(**post.model_dump())  #Here we are unpacking the dictionary

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)  #Standard way
    new_post = models.Post(**post.model_dump())  #Unpacking the dictionary using double star
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()