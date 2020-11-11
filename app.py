from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel


app = FastAPI()

cache = {}


class InputSome(BaseModel):
    some: int


@app.get("/")
async def users():
    return {"message": "hello"}


@app.post('/cache')
async def cache_save(some: InputSome):
    global cache
    cache[some] = some.some
    return {'message': 'ok'}


@app.get('/cache')
async def cache_return():
    global cache
    return {'body': cache}


if __name__ == '__main__':
    run(app)
