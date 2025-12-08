from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional, List

app = FastAPI()

database = []


def find_todo(todo_id: int):
    todo = next((todo for todo in database if todo["id"] == todo_id), None)
    return todo


class Todo(BaseModel):
    id: int
    title: str
    desc: str
    status: Literal["pending", "done"] = "pending"
    is_active: bool


class TodoCreate(BaseModel):
    title: str
    desc: str
    status: Literal["pending", "done"] = "pending"
    is_active: Optional[bool] = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    status: Optional[Literal["pending", "done"]] = None
    is_active: Optional[bool] = None


@app.get("/todos", status_code=200, response_model=List[Todo])
def read_todos():
    active_todo = [todo for todo in database if todo["is_active"]]
    return active_todo


@app.post("/todos", status_code=201, response_model=Todo)
def add_todo(todo: TodoCreate):
    new_todo = todo.model_dump()  # 把 pydantic class 轉 dicts
    new_todo["id"] = len(database) if len(database) == 0 else database[-1]["id"] + 1
    database.append(new_todo)
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_id(todo_id: int):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="todo not found")
    return current_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="todo not found")

    update_todo = todo_update.model_dump(exclude_unset=True)
    current_todo.update(update_todo)

    return current_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="todo not found")
    current_todo["is_active"] = False
    return {"result": "success"}
