from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
import models
import schemas
from init_data import init_db
import dicttoxml


app = FastAPI()

# Папка с HTML-шаблонами
templates = Jinja2Templates(directory="templates")

# Создаём таблицы, если их нет
models.Base.metadata.create_all(bind=engine)

# Заполняем БД начальными данными
init_db()


# --- Функция для подключения к базе ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- HTML-страница (аналог Thymeleaf) ---
@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


# --- REST: XML-версия списка команд ---
@app.get("/teams/xml")
def get_teams_xml(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    data = [schemas.Team.from_orm(team).dict() for team in teams]

    xml_bytes = dicttoxml.dicttoxml(
        data,
        custom_root="teams",
        attr_type=False
    )

    return Response(content=xml_bytes, media_type="application/xml")


# --- REST: список всех команд (JSON) ---
@app.get("/teams", response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams


# --- REST: одна команда по id (JSON) ---
@app.get("/teams/{team_id}", response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    return team

# --- CRUD для Book ---

@app.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing:
        return {"error": "Book not found"}

    existing.title = book.title
    existing.author = book.author
    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    existing = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing:
        return {"error": "Book not found"}

    db.delete(existing)
    db.commit()
    return {"message": "Book deleted successfully"}