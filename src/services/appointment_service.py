from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from src.models.appointment import Appointment
from src.models.doctor import Doctor

def create_appointment(db: Session, appointment):
    if appointment.start_time.tzinfo is None:
        raise HTTPException(status_code=400, detail="Datetime must be timezone-aware")

    if appointment.start_time <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Appointment must be in the future")

    if not 15 <= appointment.duration_minutes <= 180:
        raise HTTPException(status_code=400, detail="Invalid duration")

    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor or not doctor.active:
        raise HTTPException(status_code=400, detail="Doctor inactive or not found")

    end_time = appointment.start_time + timedelta(minutes=appointment.duration_minutes)

    conflict = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        and_(
            Appointment.start_time < end_time,
            (Appointment.start_time +
             timedelta(minutes=Appointment.duration_minutes)) > appointment.start_time
        )
    ).first()

    if conflict:
        raise HTTPException(status_code=409, detail="Overlapping appointment")

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
