from library_resource import LibraryResource


class Book(LibraryResource):
    def __init__(self, book_id, title, author):
        super().__init__(book_id)

        self.title = title
        self.author = author
        self.available = True

    def display_info(self):
        return (
            f"Book ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Available: {self.available}"
        )

    def __repr__(self):
        return (
            f"Book(id='{self.id}', "
            f"title='{self.title}', "
            f"author='{self.author}', "
            f"available={self.available})"
        )


class EBook(Book):
    def __init__(self, book_id, title, author, file_size):
        super().__init__(book_id, title, author)
        self.file_size = file_size

    def display_info(self):
        return (
            f"EBook ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"File Size: {self.file_size} MB, "
            f"Available: {self.available}"
        )


class AudioBook(Book):
    def __init__(self, book_id, title, author, duration):
        super().__init__(book_id, title, author)
        self.duration = duration

    def display_info(self):
        return (
            f"AudioBook ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Duration: {self.duration} minutes, "
            f"Available: {self.available}"
        )