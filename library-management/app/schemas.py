from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_borrowed: int
    borrower_id: int | None = None

    class Config:
        from_attributes = True

class ReaderBase(BaseModel):
    name: str
    reader_id: int

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True
