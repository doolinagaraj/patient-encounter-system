from pydantic import BaseModel


class DoctorCreate(BaseModel):
    full_name: str
    specialization: str


class DoctorRead(DoctorCreate):
    id: int
    active: bool

    class Config:
        orm_mode = True
