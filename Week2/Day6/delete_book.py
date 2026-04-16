from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app=FastAPI()


class Books:
    id: int
    title: str
    author: str
    description: str
    rating: int


    #Constructor is called
    def __init__(self, id, title, author, description, rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating


class BookRequest(BaseModel): #Pydantic model
    # id: int
    id: Optional[int]=Field(description="Id is not needed for create", default=None)
    title: str = Field(min_length=3)  # Field Validation
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ft=0, lt=6)

# The json_schema_extra field allows adding examples that appear in Swagger UI for better usability.
# model_config in Pydantic is used to customize model behavior and enhance API documentation.
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5
            }
        }
    }

BOOKS=[
    Books(1, "Space", "Thomas", "Very nice book", 5),
    Books(2, "Space1", "Thomas", "Very classic book", 4),
    Books(3, "Space2", "Thomas", "Average book", 3),
    Books(4, "Hp1", "Thomas", "Good Book", 3),
    Books(5, "Hp2", "Thomas","Can improve", 3)
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break
