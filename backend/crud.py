from sqlalchemy.orm import Session
from backend import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.generate_unique(db, 5)
    secret_key = f"{key}_{keygen.generate_key(8)}"
    db_url = models.URL(target_url = url.target_url, key = key, secret_key = secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (db.query(models.URL)
            .filter(models.URL.key == url_key, models.URL.is_active)
            .first())

def get_db_url_by_secret_key(db: Session, url_secret_key: str) -> models.URL:
    return (db.query(models.URL)
            .filter(models.URL.secret_key == url_secret_key, models.URL.is_active)
            .first())

def get_admin_info(db: Session, url_secret_key: str) -> models.URL:
    return (db.query(models.URL)
            .filter(models.URL.secret_key == url_secret_key)
            .first())

def update_click_counter(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_url_by_secret_key(db: Session, url_secret_key: str) -> models.URL:
    db_url = get_db_url_by_secret_key(db, url_secret_key)
    if (db_url):
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url