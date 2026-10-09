
from abc import ABC, abstractmethod


class LibraryResource(ABC):
    def __init__(self, resource_id):
        self.id = resource_id

    @abstractmethod
    def display_info(self):
        """Return a readable description of the resource."""
        pass
