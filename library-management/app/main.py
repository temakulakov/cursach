from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.post("/readers/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db=db, reader=reader)

@app.get("/readers/{reader_id}", response_model=schemas.Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = crud.get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader

@app.get("/readers/", response_model=list[schemas.Reader])
def read_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    readers = crud.get_readers(db, skip=skip, limit=limit)
    return readers

@app.put("/books/{book_id}/borrow")
def borrow_book(book_id: int, borrow_data: schemas.BorrowBook, db: Session = Depends(get_db)):
    db_book = crud.update_book_borrow_status(db, book_id, borrow_data.borrower_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}/return")
def return_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.return_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
