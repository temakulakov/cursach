from sqlalchemy.orm import Session
from . import models, schemas

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

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

def get_reader(db: Session, reader_id: int):
    return db.query(models.Reader).filter(models.Reader.reader_id == reader_id).first()

def create_reader(db: Session, reader: schemas.ReaderCreate):
    db_reader = models.Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader
