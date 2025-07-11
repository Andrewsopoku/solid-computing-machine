import csv
from datetime import datetime

def parse_csv_line(line: str):
    try:
        parts = list(csv.reader([line]))[0]
        username = parts[0].strip()
        email = parts[1].strip()
        signup_date = datetime.strptime(parts[2].strip(), "%Y-%m-%d")
        return username, email, signup_date
    except Exception as e:
        raise ValueError(f"Malformed line: {line}") from e


def is_valid_email(email: str):
    return "@" in email and "." in email.split("@")[-1]
