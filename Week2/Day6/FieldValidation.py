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

@app.post("/create_book")
async def create_book(book_request: BookRequest): #book_request is the data coming from user (gets stored)
    # ** takes key-value pairs and pack/unpack them
    # Accept any number of named arguments (key-value pairs)
    new_book = Books(**book_request.dict()) #Unpack dictionary into arguments and convert it to a Book object
    BOOKS.append(find_book_id(new_book)) #add new book to list
    
def find_book_id(book:Books):
    # if len(BOOKS)>0:
    #     book.id=BOOKS[-1].id + 1
    # else:
    #     book.id=1
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book




# id gets automatically assigned to data even if not mentioned