from datetime import datetime
from pydantic import ValidationError
from src.schemas.appointment import AppointmentCreate

def test_timezone_required():
    try:
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=datetime.now(),
            duration_minutes=30
        )
        assert False
    except ValidationError:
        assert True
