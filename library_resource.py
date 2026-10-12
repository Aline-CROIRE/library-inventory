
"""Base classes for library resources."""

from abc import ABC, abstractmethod


class LibraryResource(ABC):
    """Abstract base class for resources managed by the library."""

    def __init__(self, resource_id: str) -> None:
        """Initialize a resource with a validated ID."""
        self.id = resource_id

    @property
    def id(self) -> str:
        """Return the resource ID."""
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """Validate and store the resource ID."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Resource ID must be a non-empty string.")
        self.__id = value.strip()

    @abstractmethod
    def display_info(self) -> str:
        """Return a readable description of the resource."""
        raise NotImplementedError
