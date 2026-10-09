
from library_resource import LibraryResource


class Book(LibraryResource):
    def __init__(self, book_id, title, author, available=True):
        super().__init__(book_id)
        self.title = title
        self.author = author
        self.available = available

    def display_info(self):
        status = "Available" if self.available else "Borrowed"
        return (
            f"Book ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, Status: {status}"
        )

    def __repr__(self):
        return (
            f"Book(id={self.id!r}, title={self.title!r}, "
            f"author={self.author!r}, available={self.available!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.id == other.id


class EBook(Book):
    def __init__(self, book_id, title, author, file_size, available=True):
        super().__init__(book_id, title, author, available)
        self.file_size = file_size

    def display_info(self):
        return (
            f"EBook ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, File size: {self.file_size} MB, "
            f"Available: {self.available}"
        )


class AudioBook(Book):
    def __init__(self, book_id, title, author, duration, available=True):
        super().__init__(book_id, title, author, available)
        self.duration = duration

    def display_info(self):
        return (
            f"AudioBook ID: {self.id}, Title: {self.title}, "
            f"Author: {self.author}, Duration: {self.duration} minutes, "
            f"Available: {self.available}"
        )
