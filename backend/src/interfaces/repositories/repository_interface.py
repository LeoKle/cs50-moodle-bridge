from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class IRepository[T](ABC):
    """Generic repository interface for CRUD operations."""

    @abstractmethod
    def create(self, data: T) -> T: ...

    @abstractmethod
    def get(self, item_id: str) -> T | None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def update(self, item_id: str, data: T) -> T | None: ...

    @abstractmethod
    def delete(self, item_id: str) -> bool: ...
