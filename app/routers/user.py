from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, update, delete
from slugify import slugify
from app.schemas import CreateUser, UpdateUser
from app.backend.db import SessionLocal


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create")
async def create_user(create_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    db.execute(insert(User).values(name=create_user.name,
                                   parent_id=create_user.parent_id,
                                   slug=slugify(create_user.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


from sqlalchemy import select


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.is_active == True)).all()
    return users


@router.put("/update/user")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: CreateUser):
    user = db.scalars(select(User).where(User.is_active == user_id)).all()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(
        update(User).where(User.id == user_id).values(
            username=update_user.username,
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age)
    )
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User update is successful'
    }


@router.delete("/delete/user")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    db.execute(delete(User).where(User.id == user_id).values(is_activ=False))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User delete is successful'
    }
