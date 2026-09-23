from fastapi import APIRouter,status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2,schemas
from typing import List
from datetime import datetime, timedelta , timezone


router = APIRouter(
    prefix = "/issues",
    tags = ['issues']
)

@router.post("/", status_code = status.HTTP_201_CREATED , response_model = schemas.ResponseBook)
async def issue_book(bookissue : schemas.Issuebooks, db : Session = Depends(get_db),current_user = Depends(oauth2.normal_user)):
    book = db.query(models.Post).filter(models.Post.id == bookissue.book_id).first()
    if book is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The book with the id {bookissue.book_id} is not found in the database")
    if book.available_copies == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The book of id {bookissue.book_idid} is already issued and currently unavailable")
    issued_time = datetime.now(timezone.utc)
    due_time = datetime.now(timezone.utc) + timedelta(days=15)

    newbook = models.Bookissue(user_id = current_user.id,book_id = bookissue.book_id,issued_at = issued_time,due_date = due_time)
    db.add(newbook)
    book.available_copies = book.available_copies - 1
    db.commit()
    db.refresh(newbook)
    return newbook
@router.put("/return/{id}")
async def return_book(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.normal_user)):
    issue = db.query(models.Bookissue).filter(models.Bookissue.id == id).first()
    if issue is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The issue record not found")
    if issue.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail = "You cannot return another user books")
    if issue.returned_at is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "You have already returned the book")
    book = db.query(models.Post).filter(models.Post.id == issue.book_id).first()
    issue.returned_at = datetime.now(timezone.utc) 
    book.available_copies = book.available_copies + 1
    book.available = True
    db.commit()
    db.refresh(issue)
    return issue
@router.get("/mybooks",response_model=List[schemas.MyBookResponse])
async def my_books(db: Session = Depends(get_db),current_user = Depends(oauth2.normal_user)):
    issued_books = db.query(
        models.Bookissue.id,
        models.User.id.label("user_id"),
        models.User.name.label("user_name"),
        models.Post.id.label("book_id"),
        models.Post.title.label("book_name"),
        models.Bookissue.issued_at,
        models.Bookissue.due_date,
        models.Bookissue.returned_at
    ).join(
        models.User,
        models.Bookissue.user_id == models.User.id
    ).join(
        models.Post,
        models.Bookissue.book_id == models.Post.id
    ).filter(
        models.Bookissue.user_id == current_user.id
    ).all()

    return [
        {
            "issue_id": issue.id,
            "user_id": issue.user_id,
            "user_name": issue.user_name,
            "book_id": issue.book_id,
            "book_name": issue.book_name,
            "issued_at": issue.issued_at,
            "due_date": issue.due_date,
            "returned_at": issue.returned_at
        }
        for issue in issued_books
    ]
@router.get("/all",response_model = List[schemas.MyBookResponse])
async def all_books(db: Session = Depends(get_db),current_user = Depends(oauth2.admin_user)):
    issued_books = db.query(
        models.Bookissue.id,
        models.User.id.label("user_id"),
        models.User.name.label("user_name"),
        models.Post.id.label("book_id"),
        models.Post.title.label("book_name"),
        models.Bookissue.issued_at,
        models.Bookissue.due_date,
        models.Bookissue.returned_at
    ).join(
        models.User,
        models.Bookissue.user_id == models.User.id
    ).join(
        models.Post,
        models.Bookissue.book_id == models.Post.id
    ).all()

    return [
        {
           "issue_id": issue.id,
            "user_id": issue.user_id,
            "user_name": issue.user_name,
            "book_id": issue.book_id,
            "book_name": issue.book_name,
            "issued_at": issue.issued_at,
            "due_date": issue.due_date,
            "returned_at": issue.returned_at
        }
        for issue in issued_books
    ]