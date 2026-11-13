from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.student import StudentCreate, StudentOut
from app.services import student_service
from app.models.user import User

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.create_student(db, student)

@router.get("/", response_model=list[StudentOut])
def get_all_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.get_all_students(db, skip=skip, limit=limit)

@router.get("/search", response_model=list[StudentOut])
def search_by_department(
    department: str = Query(..., min_length=1, description="Search by department name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.search_students_by_department(db, department)

@router.get("/{student_id}", response_model=StudentOut)
def get_student_by_id(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.get_student_by_id(db, student_id)
