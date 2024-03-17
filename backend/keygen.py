import string, secrets
from sqlalchemy.orm import Session
from backend.crud import get_db_url_by_key

def generate_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def generate_unique(db: Session, length: int) -> str:
    key = generate_key(length)
    while (get_db_url_by_key(db, key)):
        key = generate_key(length)
    return key