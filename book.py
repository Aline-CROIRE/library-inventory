
"""Book models for the library."""

from library_resource import LibraryResource


class Book(LibraryResource):
    """Represent a physical or general library book."""

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        available: bool = True,
    ) -> None:
        """Initialize a book with its details and availability."""
        super().__init__(book_id)
        self.title = title
        self.author = author
        self.available = available

    @property
    def title(self) -> str:
        """Return the book title."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Validate and set the book title."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Book title must be a non-empty string.")
        self.__title = value.strip()

    @property
    def author(self) -> str:
        """Return the author's name."""
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        """Validate and set the author's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author name must be a non-empty string.")
        self.__author = value.strip()

    @property
    def available(self) -> bool:
        """Return whether the book is available."""
        return self.__available

    @available.setter
    def available(self, value: bool) -> None:
        """Accept only actual Boolean availability values."""
        if not isinstance(value, bool):
            raise ValueError("Availability must be True or False.")
        self.__available = value

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Create the appropriate book object from a dictionary."""
        book_type = data.get("type", "book")

        if book_type == "ebook":
            return EBook(
                book_id=data["id"],
                title=data["title"],
                author=data["author"],
                file_size=data["file_size"],
                available=data.get("available", True),
            )

        if book_type == "audiobook":
            return AudioBook(
                book_id=data["id"],
                title=data["title"],
                author=data["author"],
                duration=data["duration"],
                available=data.get("available", True),
            )

        if book_type != "book":
            raise ValueError(f"Unknown book type: {book_type}")

        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            available=data.get("available", True),
        )

    def to_dict(self) -> dict:
        """Convert the book into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available": self.available,
            "type": "book",
        }

    def display_info(self) -> str:
        """Return a readable description of the book."""
        status = "Available" if self.available else "Borrowed"
        return (
            f"Book ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, Status: {status}"
        )

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (
            f"{type(self).__name__}(id={self.id!r}, "
            f"title={self.title!r}, author={self.author!r}, "
            f"available={self.available!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare books by their IDs."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.id == other.id


class EBook(Book):
    """Represent an electronic book."""

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        file_size: float,
        available: bool = True,
    ) -> None:
        """Initialize an ebook with its file size in megabytes."""
        super().__init__(book_id, title, author, available)
        self.file_size = file_size

    @property
    def file_size(self) -> float:
        """Return the ebook's file size in megabytes."""
        return self.__file_size

    @file_size.setter
    def file_size(self, value: float) -> None:
        """Validate and set the ebook's file size."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("File size must be a positive number.")
        if value <= 0:
            raise ValueError("File size must be a positive number.")
        self.__file_size = float(value)

    def to_dict(self) -> dict:
        """Convert the ebook into a JSON-compatible dictionary."""
        data = super().to_dict()
        data["type"] = "ebook"
        data["file_size"] = self.file_size
        return data

    def display_info(self) -> str:
        """Return a readable description of the ebook."""
        status = "Available" if self.available else "Borrowed"
        return (
            f"EBook ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, File size: {self.file_size} MB, "
            f"Status: {status}"
        )


class AudioBook(Book):
    """Represent an audiobook."""

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        duration: int,
        available: bool = True,
    ) -> None:
        """Initialize an audiobook with its duration in minutes."""
        super().__init__(book_id, title, author, available)
        self.duration = duration

    @property
    def duration(self) -> int:
        """Return the audiobook duration in minutes."""
        return self.__duration

    @duration.setter
    def duration(self, value: int) -> None:
        """Validate and set the audiobook duration."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Duration must be a positive integer.")
        if value <= 0:
            raise ValueError("Duration must be a positive integer.")
        self.__duration = value

    def to_dict(self) -> dict:
        """Convert the audiobook into a JSON-compatible dictionary."""
        data = super().to_dict()
        data["type"] = "audiobook"
        data["duration"] = self.duration
        return data

    def display_info(self) -> str:
        """Return a readable description of the audiobook."""
        status = "Available" if self.available else "Borrowed"
        return (
            f"AudioBook ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, Duration: {self.duration} minutes, "
            f"Status: {status}"
        )
