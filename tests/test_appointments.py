from datetime import datetime, timedelta, timezone
from src.schemas.appointment import AppointmentCreate

def test_valid_appointment_schema():
    AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
        duration_minutes=30
    )
