import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from backend import models, schemas
from backend.database import LocalSession, engine

from backend import keygen
from backend.crud import *

from backend.config import get_settings

api = FastAPI()
models.Base.metadata.create_all(bind=engine)

### <-- Helper-Functions -->

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL: \"{request.url}\" does not exist!"
    raise HTTPException(status_code=404, detail=message)

### <-- API-Processing -->

@api.get("/")
def read_root():
    return "This's root 'directory' of our site."

@api.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("You provided invalid URL!")

    db_url = create_db_url(db, url)
    db_url.url = db_url.key
    db_url.secret_url = db_url.secret_key

    return db_url

@api.get("/{url_key}")
def redirect_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if (db_url := get_db_url_by_key(db, url_key)):
        update_click_counter(db, db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@api.get("/check/{url_key}")
def check_shortened_url_destination(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if (db_url := get_db_url_by_key(db, url_key)):
        return {"detail": f"Shortened URL [{get_settings().base_url}/{db_url.key}] forwards to [{db_url.target_url}]"}
    else:
        raise_not_found(request)

@api.get("/admin/{secret_key}", response_model=schemas.URLInfo)
def admin_info(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if (db_url := get_admin_info(db, secret_key)):
        db_url.url = f"{get_settings().base_url}/{db_url.key}"
        db_url.secret_url = f"{get_settings().base_url}/admin/{db_url.secret_key}"
        return db_url
    else:
        return raise_not_found(request)
    
@api.delete("/admin/deactivate/{secret_key}")
def deactivate_url(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if (db_url := deactivate_url_by_secret_key(db, secret_key)):
        message = f"Successfully removed shortened URL: {get_settings().base_url}/{db_url.key} -> {db_url.target_url}"
        return {"detail": message}
    else:
        raise_not_found(request)