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
#DELETE
@app.delete("/books/delete_book/{book_title}") #here we have .deleted method with respect to our API endpoint and we are passing the book title as a path parameter
async def delete_book(book_title:str):
    for i in range(len(Books)):
        if Books[i].get("Title").casefold()==book_title.casefold():
            Books.pop(i)  #pop method is used to remove the book from the list of books via indexing
            break