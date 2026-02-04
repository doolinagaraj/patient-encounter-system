from pydantic import BaseModel, EmailStr


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None


class PatientRead(PatientCreate):
    id: int

    class Config:
        orm_mode = True
