import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas import schema
from database import models


def get_all(db: Session):
    result = db.query(models.User).all()

    return result


def get_usrer_via_email(email: str, db: Session):
    try:
        result = db.query(
            models.User.id,
            models.User.name,
            models.User.surname,
            models.User.email,
            models.User.created_on,
            models.Role.role_name
        ).join(
            models.Role,
            models.User.role_id == models.Role.id_role
        ).where(
            models.User.email == email
        ).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail=f'Not fount user {email}')
    return result


def create_role(new_role: str, db: Session):

    role = models.Role(role_name=new_role)
    db.add(role)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f'Invalide data to save')

    db.refresh(role)

    return role


def change_privileges(new_role: schema.NewPrivilegesIn, db):

    try:
        db.query(models.User).filter(
            models.User.email == new_role.email
        ).update({"role_id": new_role.new_prewiliges})
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f'Privileges id={new_role.new_prewiliges} does\'t exist')

    db.commit()


def delete_user(email: str, db):

    db.query(models.User).filter(
        models.User.email == email
    ).delete()
    db.commit()


def add_user(new_user, db):

    user_data = new_user.dict()
    user = models.User(**user_data)

    try:
        db.add(user)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail='Write the correct data. Email exists or id_role does not exist')

    db.refresh(user)

    return user


def get_roles(db):
    result = db.query(models.Role).all()

    return result
