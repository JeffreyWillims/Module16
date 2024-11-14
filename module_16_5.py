from fastapi import FastAPI, Body, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from typing import List, Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import asyncio
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int



@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})



@app.get("/user/{user_id}")
async def get_user_page(request: Request,
                        user_id: Annotated[int, Path(ge=1, le=100,
                        description='Enter User ID', example="1")]) -> HTMLResponse:
        for user in users:
            if int(user.id) == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": user})
        raise HTTPException(status_code=404, detail="User was not found")


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100,
                                     description='Enter User ID', example="1")],
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description='Enter username', example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:

    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example="1")]) -> User:
    for  user in users:
        if user.id == user_id:
            users.remove(user)
            return user
        return f"User{user_id} has been deleted"
    raise HTTPException(status_code=404, detail="User was not found")


if __name__ == "__main__":
    asyncio.run(uvicorn.run(app, host="127.0.0.1", port=8000, loop="asyncio"))