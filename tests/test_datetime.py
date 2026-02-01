from datetime import datetime, timezone
from pydantic import ValidationError
from src.schemas.appointment import AppointmentCreate


def test_timezone_required():
    try:
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=datetime.now(),
            duration_minutes=30,
        )
        assert False
    except ValidationError:
        assert True


def test_duration_too_short():
    try:
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=datetime.now(timezone.utc),
            duration_minutes=10,
        )
        assert False
    except ValidationError:
        assert True


def test_duration_too_long():
    try:
        AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            start_time=datetime.now(timezone.utc),
            duration_minutes=240,
        )
        assert False
    except ValidationError:
        assert True


def test_invalid_patient_id():
    try:
        AppointmentCreate(
            patient_id=0,
            doctor_id=1,
            start_time=datetime.now(timezone.utc),
            duration_minutes=30,
        )
        assert False
    except ValidationError:
        assert True


def test_invalid_doctor_id():
    try:
        AppointmentCreate(
            patient_id=1,
            doctor_id=-5,
            start_time=datetime.now(timezone.utc),
            duration_minutes=30,
        )
        assert False
    except ValidationError:
        assert True


def test_start_time_timezone_ok():
    appt = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc),
        duration_minutes=30,
    )
    assert appt.start_time.tzinfo is not None


def test_duration_boundary_values():
    a_min = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc),
        duration_minutes=15,
    )
    a_max = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc),
        duration_minutes=180,
    )
    assert a_min.duration_minutes == 15
    assert a_max.duration_minutes == 180
