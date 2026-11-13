from pydantic import BaseModel, EmailStr
from app.schemas.department import DepartmentOut

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    department_id: int

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    department: DepartmentOut

    class Config:
        from_attributes = True
