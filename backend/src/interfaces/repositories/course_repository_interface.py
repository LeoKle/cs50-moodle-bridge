from abc import ABC

from interfaces.repositories.repository_interface import IRepository
from models.course import Course


class ICourseRepository(IRepository[Course], ABC):
    pass
