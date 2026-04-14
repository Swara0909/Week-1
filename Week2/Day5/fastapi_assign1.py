from fastapi import FastAPI

app = FastAPI()

Books = [
    {"title": "Book1", "author": "Author1"},
    {"title": "Book2", "author": "Author2"},
    {"title": "Book3", "author": "Author1"},
]

@app.get("/books/search_author/")
async def search_by_author(author: str):
    results = []

    for book in Books:
        if book["author"].lower() == author.lower():
            results.append(book)

    return results