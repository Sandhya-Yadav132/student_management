from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.departement import Department
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentOut

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Department).filter(
        (Department.name == dept.name) | (Department.code == dept.code)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name or code already exists",
        )
    new_dept = Department(**dept.model_dump())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/", response_model=list[DepartmentOut])
def get_all_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Department).all()
