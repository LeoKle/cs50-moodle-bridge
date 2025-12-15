from interfaces.repositories.course_repository_interface import ICourseRepository
from models.course import Course


class MockCourseRepository(ICourseRepository):
    def __init__(self):
        self._data: dict[str, Course] = {}

    def create(self, data: Course) -> Course:
        self._data[data.id] = data
        return data

    def get(self, item_id: str) -> Course | None:
        return self._data.get(item_id)

    def get_all(self) -> list[Course]:
        return list(self._data.values())

    def update(self, item_id: str, data: Course) -> Course | None:
        if item_id not in self._data:
            return None

        self._data[item_id] = data
        return self._data[item_id]

    def delete(self, item_id: str) -> bool:
        if item_id in self._data:
            self._data.pop(item_id)
            return True
        return False
