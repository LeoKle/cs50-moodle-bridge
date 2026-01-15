from abc import ABC, abstractmethod
from typing import BinaryIO


class IGitHubService(ABC):
    @abstractmethod
    def import_github_names(file: BinaryIO): ...
