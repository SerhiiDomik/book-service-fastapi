from fastapi import FastAPI
from src.database.session import engine, Base
from src.routes.auth import router as auth_router
from src.routes.books import router as books_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(books_router, prefix="/books", tags=["Books"])
