from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import or_

router = APIRouter(
    prefix = "/books",
    tags = ['books']
)

@router.get("/", response_model = List[schemas.BookResponse])
async def get_books(db : Session = Depends(get_db),Limit : int = 10, search : Optional[str]= ""):

    books = db.query(models.Post).filter(or_(models.Post.title.ilike(f"{search}%"),(models.Post.author.ilike(f"{search}%")))).limit(Limit).all()
    return books

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.BookResponse)
async def addbook(book : schemas.Addbook, db: Session = Depends(get_db), current_user = Depends(oauth2.admin_user)):
    existing = db.query(models.Post).filter(models.Post.title == book.title , models.Post.author == book.author).first()
    if existing:
        existing.total_copies = (existing.total_copies + book.total_copies)
        existing.available_copies = (existing.available_copies + book.total_copies)
        db.commit()
        db.refresh(existing)
        return existing
    new_book = models.Post(**book.dict(exclude = {"available_copies"}),available_copies = book.total_copies)#That's useful only when the dictionary keys match the SQLAlchemy model attributes.
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/{id}", response_model= schemas.BookResponse)
async def id_books(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Post).filter(models.Post.id == id).first()
    print(book)
    if book is None:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The id doesn't exist ")
    return book


@router.delete("/{id}")
async def delete_books(id: int, db: Session = Depends(get_db),current_user = Depends(oauth2.admin_user)):
    deleted_book = db.query(models.Post).filter(models.Post.id == id)
    if deleted_book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"The {id} which u want to delete is not found")
    deleted_book.delete(synchronize_session=False)
    db.commit()
    return{"data" : " Post Deleted"}

@router.delete("/{id}/copies")
async def delete_copies(id : int,copies: int,db:Session = Depends(get_db),current_user = Depends(oauth2.admin_user)):
    deleted_copies = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_copies is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The {id} which u want to delete is not found")
    if copies <= 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The Book Copies which u want to delete must be zero")
    if copies > deleted_copies.available_copies:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"There are only {deleted_copies.available_copies} copies are currently available")
    deleted_copies.total_copies -= copies
    deleted_copies.available_copies -= copies
    db.commit()
    db.refresh(deleted_copies)
    return deleted_copies

@router.put("/{id}")
async def update_data(id : int,book : schemas.Addbook,db : Session = Depends(get_db),current_user = Depends(oauth2.admin_user)):
    updating_book = db.query(models.Post).filter(models.Post.id == id)
    if updating_book.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The {id} which you want update is not found")
    updating_book.update(book.dict(),synchronize_session=False)
    db.commit()
    updated_book = db.query(models.Post).filter(
        models.Post.id == id
    ).first()
    return updated_book
