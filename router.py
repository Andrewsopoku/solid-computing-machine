from fastapi import APIRouter, UploadFile, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from utils import parse_csv_line, is_valid_email
from models import User
from datetime import datetime
import csv

router = APIRouter()

@router.post("/bulk-users/upload")
def upload_bulk_users(file: UploadFile, db: Session = get_db()):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = file.file.read().decode("utf-8")
    lines = content.split("\n")

    success_count = 0
    failure_count = 0
    failed_rows = []

    for i, line in enumerate(lines[1:], start=2):  # Skip header
        if not line.strip():
            continue
        try:
            username, email, signup_date = parse_csv_line(line)

            if not is_valid_email(email):
                raise ValueError("Invalid email format")

            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                raise ValueError("User already exists")

            user = User(
                username=username,
                email=email,
                signup_date=signup_date
            )
            db.add(user)
            db.commit()
            success_count += 1

        except Exception as e:
            failure_count += 1
            failed_rows.append({
                "line": i,
                "error": str(e),
                "raw": line
            })

    return {
        "summary": {
            "total": len(lines) - 1,
            "successful": success_count,
            "failed": failure_count,
        },
        "failures": failed_rows
    }
