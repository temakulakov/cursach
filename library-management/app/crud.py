from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

# Создание книги
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="ISBN already exists")
    return db_book

# Получение книги по ID
def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Получение всех книг
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

# Обновление статуса книги (выдача)
def update_book_borrow_status(db: Session, book_id: int, borrower_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.is_borrowed = 1
    db_book.borrower_id = borrower_id
    db.commit()
    db.refresh(db_book)
    return db_book

# Возврат книги
def return_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.is_borrowed = 0
    db_book.borrower_id = None
    db.commit()
    db.refresh(db_book)
    return db_book

# Создание читателя
def create_reader(db: Session, reader: schemas.ReaderCreate):
    db_reader = models.Reader(**reader.dict())
    try:
        db.add(db_reader)
        db.commit()
        db.refresh(db_reader)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Reader ID already exists")
    return db_reader

# Получение читателя по ID
def get_reader(db: Session, reader_id: int):
    reader = db.query(models.Reader).filter(models.Reader.reader_id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

# Получение всех читателей
def get_readers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Reader).offset(skip).limit(limit).all()
