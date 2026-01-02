from abc import ABC, abstractmethod


class IGitHubClientResolver(ABC):
    @abstractmethod
    def get_user_id(self, username: str) -> int | None:
        """
        Returns the GitHub user ID, given the GitHub username

        :param username: GitHub username
        :type username: str
        :return: GitHub user id
        :rtype: int
        """
        ...
