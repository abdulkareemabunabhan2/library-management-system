from fastapi import FastAPI

from library.presntation.routes import books, borrow, members

app = FastAPI()

# routes
app.include_router(books.router, prefix='/books', tags=['books'])
app.include_router(members.router, prefix='/members', tags=['members'])
app.include_router(borrow.router, tags=['borrow'])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
