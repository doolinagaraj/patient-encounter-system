from datetime import datetime, timedelta, timezone
import pytest
from src.schemas.appointment import AppointmentCreate
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from src.database import SessionLocal
from src.services import patient_service, doctor_service, appointment_service
from fastapi import HTTPException


def test_valid_appointment_schema():
    AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
        duration_minutes=30,
    )


def test_overlapping_appointments_conflict():
    db = SessionLocal()
    try:
        unique = datetime.now().timestamp()
        patient = patient_service.create_patient(
            db,
            PatientCreate(
                first_name="T", last_name="U", email=f"test{unique}@example.com"
            ),
        )
        doctor = doctor_service.create_doctor(
            db, DoctorCreate(full_name="Dr Test", specialization="General")
        )
        start = datetime.now(timezone.utc) + timedelta(days=1)
        from src.models.appointment import Appointment

        scheduled = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            start_time=start,
            duration_minutes=30,
        )
        db.add(scheduled)
        db.commit()

        a2 = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            start_time=start + timedelta(minutes=10),
            duration_minutes=30,
        )
        with pytest.raises(HTTPException) as excinfo:
            appointment_service.create_appointment(db, a2)
        assert excinfo.value.status_code == 409
    finally:
        db.close()
