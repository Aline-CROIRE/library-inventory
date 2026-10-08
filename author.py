class Author:
    def __init__(self, author_id, name):
        self.id = author_id
        self.name = name

    def __repr__(self):
        return f"Author(id='{self.id}', name='{self.name}')"