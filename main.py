from fastapi import FastAPI
from library.presntation.routes import books, borrow, members

app = FastAPI()

# routes
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(borrow.router, tags=["Borrow"])
@app.get("/")
def read_root():
    return {"Hello": "World"}
