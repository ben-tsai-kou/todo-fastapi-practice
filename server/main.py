from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

app = FastAPI()

fake_db = []


def find_todo(todo_id: int):
    return next((t for t in fake_db if t["id"] == todo_id), None)


class Todo(BaseModel):
    id: int
    title: str = Field(
        description="a todo title",
        title="todo title",
        examples=["Write a blog to share some new stuff"],
    )
    desc: str = Field(
        description="todo's description",
        title="todo description",
        examples=["I need to post a blog on Qiita"],
    )
    status: Literal["pending", "done"] = Field(
        description="to check the todo is pending or done",
        title="todo's status",
        examples=["pending", "done"],
    )
    is_active: bool = Field(
        description="is todo displayed or deleted",
        title="to check if todo is displayed or deleted",
    )


class TodoCreate(BaseModel):
    title: str = Field(
        min_length=10,
        max_length=500,
        description="a todo title",
        title="todo title",
        examples=["Write a blog to share some new stuff"],
    )
    desc: str = Field(
        min_length=30,
        max_length=1000,
        description="todo's description",
        title="todo description",
        examples=["I need to post a blog on Qiita"],
    )
    status: Literal["pending", "done"] = Field(
        default="pending",
        description="to check the todo is pending or done",
        title="todo's status",
        examples=["pending", "done"],
    )
    is_active: bool = Field(
        description="is todo displayed or deleted",
        title="to check if todo is displayed or deleted",
    )


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=500,
        description="a todo title",
        title="todo title",
        examples=["Write a blog to share some new stuff"],
    )
    desc: Optional[str] = Field(
        default=None,
        min_length=30,
        max_length=1000,
        description="todo's description",
        title="todo description",
        examples=["I need to post a blog on Qiita"],
    )
    status: Optional[Literal["pending", "done"]] = Field(
        default=None,
        description="to check the todo is pending or done",
        title="todo's status",
        examples=["pending", "done"],
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="is todo displayed or deleted",
        title="to check if todo is displayed or deleted",
    )


@app.get("/todos", response_model=List[Todo])
def read_todos():
    return [todo for todo in fake_db if todo["is_active"]]


@app.post("/todos", status_code=201, response_model=Todo)
def add_todo(todo: TodoCreate):
    new_todo = todo.model_dump()  # 把 pydantic class 轉 dicts
    new_todo["id"] = len(fake_db) + 1 if len(fake_db) == 0 else fake_db[-1]["id"] + 1
    fake_db.append(new_todo)
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return current_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_payload: TodoUpdate):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_payload.model_dump(exclude_unset=True)
    current_todo.update(update_data)

    return current_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    current_todo = find_todo(todo_id)
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    current_todo["is_active"] = False
    return
