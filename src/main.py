from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from src.database import Base, engine, SessionLocal
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from src.schemas.appointment import AppointmentCreate
from src.services import patient_service, doctor_service, appointment_service
from src.models.appointment import Appointment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Encounter Management System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients", status_code=201)
def create_patient(p: PatientCreate, db: Session = Depends(get_db)):
    return patient_service.create_patient(db, p)

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.get_patient(db, patient_id)

@app.post("/doctors", status_code=201)
def create_doctor(d: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create_doctor(db, d)

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_service.get_doctor(db, doctor_id)

@app.post("/appointments", status_code=201)
def create_appointment(a: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment_service.create_appointment(db, a)

@app.get("/appointments")
def list_appointments(date: date, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(
        Appointment.start_time.cast(date) == date
    ).all()
