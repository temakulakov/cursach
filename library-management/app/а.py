from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import Optional

Base = declarative_base()

class Borrowable:
    """
    Абстрактный класс, представляющий заимствуемый предмет.
    """
    def borrow(self, reader_id: int, db: Session):
        raise NotImplementedError("Метод borrow должен быть переопределен")

    def return_item(self, db: Session):
        raise NotImplementedError("Метод return_item должен быть переопределен")

class Item(Base, Borrowable):
    """
    Базовый класс для всех предметов в библиотеке.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_borrowed = Column(Integer, default=0)
    borrower_id = Column(Integer, ForeignKey("readers.id"), nullable=True)
    borrower = relationship("Reader", back_populates="borrowed_items")

    def borrow(self, reader_id: int, db: Session):
        if self.is_borrowed:
            raise HTTPException(status_code=400, detail="Item already borrowed")
        self.is_borrowed = 1
        self.borrower_id = reader_id
        db.commit()
        db.refresh(self)

    def return_item(self, db: Session):
        if not self.is_borrowed:
            raise HTTPException(status_code=400, detail="Item is not borrowed")
        self.is_borrowed = 0
        self.borrower_id = None
        db.commit()
        db.refresh(self)

class Book(Item):
    """
    Класс, представляющий книгу в библиотеке.
    """
    __tablename__ = "books"
    author = Column(String)
    isbn = Column(String, unique=True, index=True)

class Person(Base):
    """
    Базовый класс для всех людей, связанных с библиотекой.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Reader(Person):
    """
    Класс, представляющий читателя библиотеки.
    """
    __tablename__ = "readers"
    reader_id = Column(Integer, unique=True, index=True)
    borrowed_items = relationship("Item", back_populates="borrower")

    def borrow_item(self, item: Item, db: Session):
        item.borrow(self.id, db)

    def return_item(self, item: Item, db: Session):
        item.return_item(db)

class Library:
    """
    Класс, представляющий библиотеку, управляющую коллекцией книг и читателей.
    """
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_item(self, item: Base):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

    def add_reader(self, reader: Reader):
        self.add_item(reader)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.title == title).first()

    def find_reader_by_id(self, reader_id: int) -> Optional[Reader]:
        return self.db.query(Reader).filter(Reader.reader_id == reader_id).first()

    def issue_item(self, item_id: int, reader_id: int):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        reader = self.db.query(Reader).filter(Reader.reader_id == reader_id).first()
        if item and reader:
            reader.borrow_item(item, self.db)
        else:
            raise HTTPException(status_code=404, detail="Item or Reader not found")

    def return_item(self, item_id: int):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.return_item(self.db)
        else:
            raise HTTPException(status_code=404, detail="Item not found")

# Настройка базы данных
engine = create_engine("sqlite:///./test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
