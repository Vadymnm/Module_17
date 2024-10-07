from pydantic import BaseModel


class CreateUser(BaseModel):
    username:  str
    firstname: str
    lastname:  str
    slug: str
    age:  int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateTask(BaseModel):
    id: int
    title:  str
    content: str
    priority:  int


class UpdateTask(BaseModel):
    id: int
    title:  str
    content: str
    priority: int
