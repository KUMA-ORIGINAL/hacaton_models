from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/")
async def get_users(name: str):
    return


@app.get("/hello/{name}")
async def get_users(name: str):
    return {"message": f"Hello {name}"}

