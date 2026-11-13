from fastapi import FastAPI
from app.database.base import Base
from app.database.database import engine
from app.models import user, departement, student
from app.routers import auth, departements, students

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API", version="1.0.0")

app.include_router(auth.router)
app.include_router(departements.router)
app.include_router(students.router)

@app.get("/")
def health_check():
    return {"status": "running"}
