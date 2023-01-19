import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book (BaseModel):
    name: str
    price: float
    book_id: Optional[str] = uuid4().hex
    genre: Literal["fiction", "non-fiction"]

BOOK_DATABASE = []


BOOKS_FILE = "books.json"


if os.path.exists(BOOKS_FILE):
    with open (BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)


# /     -> boas vindas
@app.get("/")
async def home():
    return "Welcome to my bookstore"

# /list-books -> listar todos os livros
@app.get("/list-books")
async def list_books():
    return { "books": BOOK_DATABASE }


# /list-book-by-index/{index} -> listar 1 livro
@app.get("/list-book-by-index/{index}")
async def list_book_by_index(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(404, "Index out of range")
    else:
        return { "books": BOOK_DATABASE[index] }


# /get-random-book -> livro aleatório
@app.get("/get-random-book")
async def get_random_book():
    return  random.choice(BOOK_DATABASE)

# /add-book -> adicionar novo livro
@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    
    with open (BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
    return { "message": f'Book {book} was added' }