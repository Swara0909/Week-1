# Post request before validation
from fastapi import FastAPI, Body

app=FastAPI()


class Books:
    id: int
    title: str
    author: str
    description: str
    rating: int



    def __init__(self, id, title, author, description, rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

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

@app.post("/books/create_book")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)