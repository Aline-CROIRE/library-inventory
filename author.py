
"""Author model for the library."""

from library_resource import LibraryResource


class Author(LibraryResource):
    """Represent an author registered in the library."""

    def __init__(self, author_id: str, name: str) -> None:
        """Initialize an author with an ID and name."""
        super().__init__(author_id)
        self.name = name

    @property
    def name(self) -> str:
        """Return the author's name."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Validate and set the author's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author name must be a non-empty string.")
        self.__name = value.strip()

    @classmethod
    def from_dict(cls, data: dict) -> "Author":
        """Create an author from a JSON-compatible dictionary."""
        return cls(
            author_id=data["id"],
            name=data["name"],
        )

    def to_dict(self) -> dict:
        """Convert the author into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def display_info(self) -> str:
        """Return a readable description of the author."""
        return f"Author ID: {self.id}, Name: {self.name}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Author(id={self.id!r}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        """Compare authors by their IDs."""
        if not isinstance(other, Author):
            return NotImplemented
        return self.id == other.id
