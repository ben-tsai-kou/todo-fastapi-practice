from fastapi import FastAPI
from typing import Literal, Optional

app = FastAPI()

todos = []


@app.get("/")
def read_todos():
    active_todo = [todo for todo in todos if todo["is_display"]]
    return {"todos": active_todo}


@app.post("/")
def add_todo(title: str, desc: str, status: Literal["pending", "done"]):
    todos.append(
        {
            "id": len(todos) + 1,
            "title": title,
            "desc": desc,
            "status": status,
            "is_display": True,
        }
    )
    return {"result": "success"}


@app.get("/items/{todo_id}")
def get_todo_id(todo_id: int):
    current_todo = [todo for todo in todos if todo["id"] == todo_id]
    if not current_todo:
        return {"result": "error", "desc": "item not found."}
    return {current_todo[0]}


@app.patch("/")
def update_todo(
    todo_id: int,
    title: Optional[str],
    desc: Optional[str],
    status: Optional[Literal["pending", "done"]],
):
    current_todo = [todo for todo in todos if todo["id"] == todo_id]
    if not current_todo:
        return {"result": "error", "desc": "item not found."}

    if title:
        current_todo[0]["title"] = title
    if desc:
        current_todo[0]["desc"] = desc
    if status:
        current_todo[0]["status"] = status
    return {"result": "success"}


@app.delete("/{todo_id}")
def delete_todo(todo_id: int):
    current_todo = [
        todo for todo in todos if todo["id"] == todo_id and todo["is_display"]
    ]
    if not current_todo:
        return {"result": "error", "desc": "item not found."}
    current_todo[0]["is_display"] = False
    return {"result": "success"}
