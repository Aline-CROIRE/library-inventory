
from library_resource import LibraryResource


class Author(LibraryResource):
    def __init__(self, author_id, name):
        super().__init__(author_id)
        self.name = name

    def display_info(self):
        return f"Author ID: {self.id}, Name: {self.name}"

    def __repr__(self):
        return f"Author(id={self.id!r}, name={self.name!r})"
