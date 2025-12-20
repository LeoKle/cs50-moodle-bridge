from abc import ABC, abstractmethod


class IGitHubUserResolver(ABC):
    @abstractmethod
    def get_user_id(self, username: str) -> int:
        """
        Returns the GitHub user ID, given the GitHub username

        :param username: GitHub username
        :type username: str
        :return: GitHub user id
        :rtype: int
        """
        ...
