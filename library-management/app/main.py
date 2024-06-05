from fastapi import FastAPI, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость, которая создает и закрывает сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.put("/books/{book_id}/borrow", response_model=schemas.Book)
def borrow_book(book_id: int, borrower: schemas.BorrowRequest, db: Session = Depends(get_db)):
    return crud.update_book_borrow_status(db=db, book_id=book_id, borrower_id=borrower.borrower_id)

@app.put("/books/{book_id}/return", response_model=schemas.Book)
def return_book(book_id: int, db: Session = Depends(get_db)):
    return crud.return_book(db=db, book_id=book_id)

@app.post("/readers/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db=db, reader=reader)

@app.get("/readers/", response_model=List[schemas.Reader])
def get_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_readers(db=db, skip=skip, limit=limit)

@app.get("/readers/{reader_id}/books", response_model=List[schemas.Book])
def get_books_for_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = crud.get_reader(db=db, reader_id=reader_id)
    return reader.borrowed_books
