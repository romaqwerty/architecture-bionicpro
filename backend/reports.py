from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_session


router = APIRouter()


def parse_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")


def get_username(current_user: dict) -> str:
    return current_user.get("preferred_username") or current_user.get("sub")


def serialize_report(row) -> dict:
    return {
        "username": row.username,
        "email": row.email,
        "date_of_birth": row.date_of_birth.isoformat() if row.date_of_birth else None,
        "timestamp": row.timestamp.isoformat() if row.timestamp else None,
        "sensor_value": float(row.sensor_value) if row.sensor_value is not None else None,
    }


def fetch_reports(
    session: Session,
    username: str,
    start_dt: Optional[datetime],
    end_dt: Optional[datetime],
):
    query_text = """
        SELECT username, email, date_of_birth, timestamp, sensor_value
        FROM report
        WHERE username = :username
    """
    params = {"username": username}

    if start_dt:
        query_text += " AND timestamp >= :start_date"
        params["start_date"] = start_dt
    if end_dt:
        query_text += " AND timestamp <= :end_date"
        params["end_date"] = end_dt

    query_text += " ORDER BY timestamp ASC"
    return session.execute(text(query_text), params).fetchall()


@router.get("/reports")
def get_report(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)
    result = fetch_reports(session, get_username(current_user), start_dt, end_dt)

    if not result:
        return {
            "reports": [],
            "message": "\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u044e\u0442 \u0434\u0430\u043d\u043d\u044b\u0435 \u0437\u0430 \u043f\u0435\u0440\u0438\u043e\u0434.",
        }

    return {"reports": [serialize_report(row) for row in result]}
