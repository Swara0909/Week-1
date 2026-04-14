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
    id: int
    title: str = Field(min_length=3)  # Field Validation
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ft=0, lt=6)

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
    BOOKS.append(book_request) #add new book to list
    
# User sends data
# FastAPI receives it
# Convert to dictionary
# Create Book object
# Add to list