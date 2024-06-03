from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_borrowed: bool
    borrower_id: Optional[int] = None

    class Config:
        from_attributes = True

class ReaderBase(BaseModel):
    name: str
    reader_id: int

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int
    borrowed_books: List[Book] = []

    class Config:
        from_attributes = True
