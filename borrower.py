
"""Borrower model for the library."""

from library_resource import LibraryResource


class Borrower(LibraryResource):
    """Represent a person who borrows library books."""

    def __init__(self, borrower_id: str, name: str) -> None:
        """Initialize a borrower with an ID and name."""
        super().__init__(borrower_id)
        self.name = name

    @property
    def name(self) -> str:
        """Return the borrower's name."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Validate and set the borrower's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Borrower name must be a non-empty string.")
        self.__name = value.strip()

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        """Create a borrower from a JSON-compatible dictionary."""
        return cls(
            borrower_id=data["id"],
            name=data["name"],
        )

    def to_dict(self) -> dict:
        """Convert the borrower into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def display_info(self) -> str:
        """Return a readable description of the borrower."""
        return f"Borrower ID: {self.id}, Name: {self.name}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Borrower(id={self.id!r}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        """Compare borrowers by their IDs."""
        if not isinstance(other, Borrower):
            return NotImplemented
        return self.id == other.id
