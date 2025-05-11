from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from app import models, oauth2
from typing import List, Optional

from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import Post, PostCreate, PostOut

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Routes for post

@router.get("/", response_model=List[PostOut])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.title.contains(search)) \
        .group_by(models.Post.id) \
        .limit(limit) \
        .offset(skip) \
        .all()

    # Transform the results into the expected format
    formatted_posts = [
        {
            "Post": post,
            "Votes": votes if votes is not None else 0
        } for post, votes in results
    ]

    return formatted_posts


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.id == id) \
        .group_by(models.Post.id) \
        .first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    
    return {"Post": result[0], "Votes": result[1] if result[1] is not None else 0}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Prone to SQL Injection (The user can enter the SQL query directly into the values fields)
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})") 

    # cursor.execute(""" INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post.model_dump()) #Standard way
    # print(**post.model_dump())  #Here we are unpacking the dictionary

    # print(current_user.id)

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)  #Standard way
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())  #Unpacking the dictionary using double star
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Delete a post by ID
    """
    # Query the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check if post exists
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    
    # Check if user owns the post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    # Delete the post using the query
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()