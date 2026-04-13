from fastapi import Body, FastAPI
app=FastAPI()
Books=[
    {"Title":"Title1","Author":"Author1","category":"science"},
    {"Title":"Title2","Author":"Author2","category":"science"},
    {"Title":"Title3","Author":"Author3","category":"history"},
    {"Title":"Title4","Author":"Author4","category":"english"},
    {"Title":"Title5","Author":"Author5","category":"science"},
]

@app.get("/books")      #Requesting
async def read_all_books():
    return Books

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(Books)):
        if Books[i].get('Title').casefold()==updated_book.get('Title').casefold():  #via indexing it updates the value of the book
            Books[i]=updated_book
            