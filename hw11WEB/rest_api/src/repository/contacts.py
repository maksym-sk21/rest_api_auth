from sqlalchemy.orm import Session
from ..database.models import Contact
from ..schemas import ContactCreate, ContactUpdate
from ..database.models import User
from sqlalchemy import and_


def create_contact(db: Session, contact: ContactCreate, current_user: User):
    db_contact = Contact(**contact.dict(), user_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10):
    return db.query(Contact).filter(and_(Contact.user_id == user.id)).offset(skip).limit(limit).all()


def get_contact(db: Session, user: User, contact_id: int):
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


def update_contact(db: Session, contact_id: int, user: User, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        for attr, value in contact.dict().items():
            setattr(db_contact, attr, value) if value else None
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, user: User, contact_id: int):
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
