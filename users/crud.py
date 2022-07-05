from datetime import datetime

import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database import models


def get_user_via_email(email: str, db: Session):
    try:
        result = db.query(
            models.User.id,
            models.User.name,
            models.User.surname,
            models.User.email,
            models.User.password,
            models.User.created_on,
            models.Role.role_name
        ).join(
            models.Role,
            models.User.role_id == models.Role.id_role
        ).where(
            models.User.email == email
        ).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=401, detail=f'Not found user {email}')
    return result


def change_password(new_password: str, email: str, db: Session):

    try:
        db.query(
            models.User
        ).filter(
            models.User.email == email
        ).update(
            {
                "password": new_password
            }
        )
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f'Privileges id={email} does\'t exist')


def create_new_tag(new_tag: str, email: str, db: Session):
    user_id = db.query(models.User.id).where(models.User.email == email)
    tag = models.Tag(tag=new_tag, user_id=user_id)

    try:
        db.add(tag)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f'Tag {new_tag} already exist')

    db.refresh(tag)

    return tag


def get_tags_for_me(email: str, db: Session):
    user_id = db.query(models.User.id).where(models.User.email == email)
    tags = db.query(models.Tag).where(models.Tag.user_id == user_id).all()

    return tags


def create_new_post(new_post, db, email):
    user_id = db.query(models.User.id).where(models.User.email == email)
    tag_id = db.query(
        models.Tag.id
    ).where(
        and_(
            models.Tag.tag == new_post.tag,
            models.Tag.user_id == user_id
        )
    )

    post = models.Post(
        post=new_post.post,
        created_on=datetime.now(),
        tag_id=tag_id,
        user_id=user_id
    )

    try:
        db.add(post)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f'Wrong tag: {new_post.tag} ')

    db.refresh(post)

    return post


def get_posts(email: str, db: Session):
    user_id = db.query(models.User.id).where(models.User.email == email)
    posts = db.query(models.Post).where(models.Post.user_id == user_id).all()

    return posts


def get_posts_by_tag(email: str, tag_id: int, db: Session):
    user_id = db.query(models.User.id).where(models.User.email == email)
    posts = db.query(
        models.Post
    ).where(
        and_(
            models.Post.user_id == user_id,
            models.Post.tag_id == tag_id
        )
    ).all()

    return posts
