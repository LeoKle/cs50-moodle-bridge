from fastapi import FastAPI

from api.router import main_router
from api.v1.controllers import course, cs50_submission_problem, enrollment
from dependencies import DependencyContainer

app = FastAPI()
app.include_router(main_router)

container = DependencyContainer()
container.wire(modules=[course, enrollment, cs50_submission_problem])
