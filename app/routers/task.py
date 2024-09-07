from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from app.models import *
from app.backend.db_depends import get_db
from app.schemas import CreateTask, UpdateTask


router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no tasks'
        )
    return tasks


@router.get("/by_task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    return task


@router.get("/by_user_id")
async def task_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    return tasks

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id):
    db.execute(insert(Task).values(id=create_task.id,
                                    title=create_task.title,
                                    content=create_task.content,
                                    priority=create_task.priority,
                                    user_id=user_id,
                                    slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], update_task:UpdateTask, id: int):
    task = db.scalar(select(Task).where(Task.id == id))
    if task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no task found'
        )
    db.execute(update(Task).where(Task.id == id).
               values(title=update_task.title,
                        content=update_task.content,
                        priority=update_task.priority,
                        slug=slugify(update_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful'}


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], id: int):
    task_delete = db.scalar(select(Task).where(Task.id == id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task is not found'
        )
    db.execute(delete(Task).where(Task.id == id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful'}