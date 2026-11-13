from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    code: str

class DepartmentOut(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True
