from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from typing import Optional
from pydantic import BaseModel



books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949
    }
    ,
    {
        "id": 4,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "year": 1951
    },
    {
        "id": 5,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813
    }
]

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    
    
class BookInput(BaseModel):
    title: str
    author: str
    year: int
    

@app.get("/books")
async def get_books():
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
async def create_book(book: BookInput):
    book_id = len(books) + 1
    new_book = {
        "id": book_id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    }
    books.append(new_book)
    return new_book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookInput):
    for i in range(len(books)):
        if books[i]["id"] == book_id:
            books[i]["title"] = book.title
            books[i]["author"] = book.author
            books[i]["year"] = book.year
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i]["id"] == book_id:
            deleted_book = books.pop(i)
            return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")