from fastapi import FastAPI
from src.database import Base, engine
from src.database.session import engine
from src.routes import auth, books

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/books", tags=["Books"])
