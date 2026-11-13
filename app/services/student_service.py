from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.departement import Department
from app.schemas.student import StudentCreate

# ... keep create_student, get_all_students, get_student_by_id as they are ...

def search_students_by_department(db: Session, department_query: str) -> list[Student]:
    clean_query = department_query.strip()
    return (
        db.query(Student)
        .join(Department)
        .filter(
            or_(
                Department.name.ilike(f"%{clean_query}%"),
                Department.code.ilike(f"%{clean_query}%")
            )
        )
        .all()
    )
