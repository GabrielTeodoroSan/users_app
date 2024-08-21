from fastapi import FastAPI

from app.schemas import User, UserResponse

app = FastAPI()

@app.post('/create/', response_model=UserResponse)
def create_user(user: User):
    ...


@app.put('/update/{id}')
def update_user(user: User, id: int):
    ... 


@app.delete('/delete/{id}')
def delete_user(id: int):
    ...


@app.get('/get/{id}')
def get_user(id: int):
    ...