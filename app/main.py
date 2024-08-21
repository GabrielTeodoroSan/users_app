from fastapi import FastAPI

from app.schemas import User, UserResponse

app = FastAPI()

@app.post('/create/', response_model=UserResponse)
def create_user(user: User):
    ...
