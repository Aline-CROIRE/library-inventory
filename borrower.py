class Borrower:
    def __init__(self, borrower_id, name):
        self.id = borrower_id
        self.name = name

    def __repr__(self):
        return f"Borrower(id='{self.id}', name='{self.name}')"