from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)
    is_borrowed = Column(Integer, default=0)
    borrower_id = Column(Integer, ForeignKey("readers.id"), nullable=True)

    borrower = relationship("Reader", back_populates="borrowed_books")

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    reader_id = Column(Integer, unique=True, index=True)

    borrowed_books = relationship("Book", back_populates="borrower")
