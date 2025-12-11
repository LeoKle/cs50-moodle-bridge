from abc import ABC

from domain.models.course import Course
from interfaces.repositories import IRepository


class ICourseRepository(IRepository[Course], ABC):
    pass
