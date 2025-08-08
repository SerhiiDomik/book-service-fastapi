from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_books():
    return [{"id": 1, "title": "The Great Gatsby"}, {"id": 2, "title": "1984"}]

@router.post("/")
def create_book():
    return {"message": "Book created"}
