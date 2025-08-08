from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
