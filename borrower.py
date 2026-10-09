
from library_resource import LibraryResource


class Borrower(LibraryResource):
    def __init__(self, borrower_id, name):
        super().__init__(borrower_id)
        self.name = name

    def display_info(self):
        return f"Borrower ID: {self.id}, Name: {self.name}"

    def __repr__(self):
        return f"Borrower(id={self.id!r}, name={self.name!r})"
