from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Prone to SQL Injection (The user can enter the SQL query directly into the values fields)
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})") 

    cursor.execute(""" INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    return {'post_detail': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {
        'Data' : post_dict
    }

