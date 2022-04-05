from typing import List, Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(limit: Optional[int] = 10,
              skip: Optional[int] = 0,
              search: Optional[str] = "",
              db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):

    return (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
        .all()
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    # Prepare an entry in the database
    db.add(new_post)

    # Actually save the entry in the database
    db.commit()

    # Retrive the new_post just created and store it back in the new_post variable.
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                  .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                  .group_by(models.Post.id)
                  .filter(models.Post.id == id))

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # This only creates the query, it doesn't execute it.
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, p: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post_query.update(**p.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
