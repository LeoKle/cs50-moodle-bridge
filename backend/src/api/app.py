from fastapi import FastAPI

from api.router import main_router

app = FastAPI()
app.include_router(main_router)


@app.get("/")
def get_root():
    return ""
