from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # we can add bycrypt for hash
    fake_hashed_password = user.password
    db_user = models.User(name=user.name, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    db_user.email = user.email
    db_user.name  = user.name
    db.commit()
    db.refresh(db_user)
    return db_user

def user_auth(db: Session, email: str, password: str):
    user_data = db.query(models.User).filter(models.User.email == email, models.User.hashed_password == password).first()
    if user_data:
        user_data.last_login = datetime.now()
        db.commit()
        db.refresh(user_data)
    return user_data