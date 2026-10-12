
"""Library operations using object-oriented resource models."""

from datetime import datetime

from author import Author
from book import Book
from borrower import Borrower
from utils import load_library, save_library, generate_id


def _load_library_objects() -> dict:
    """Load JSON records and convert resources into Python objects."""
    data = load_library()

    return {
        "books": [Book.from_dict(item) for item in data["books"]],
        "authors": [Author.from_dict(item) for item in data["authors"]],
        "borrowers": [
            Borrower.from_dict(item) for item in data["borrowers"]
        ],
        "borrowings": data["borrowings"],
    }


def _save_library_objects(library: dict) -> None:
    """Convert resource objects to dictionaries and save the library."""
    data = {
        "books": [book.to_dict() for book in library["books"]],
        "authors": [author.to_dict() for author in library["authors"]],
        "borrowers": [
            borrower.to_dict() for borrower in library["borrowers"]
        ],
        "borrowings": library["borrowings"],
    }
    save_library(data)


def _find_book(library: dict, user_input: str) -> Book | None:
    """Find a book by its displayed number or full ID."""
    value = user_input.strip()

    if value.isdigit():
        book_id = f"BK{int(value):03d}"
    else:
        book_id = value

    return next(
        (book for book in library["books"] if book.id == book_id),
        None,
    )


def add_book() -> None:
    """Add a book and register its author if necessary."""
    print("\nAdd a New Book")

    library = _load_library_objects()

    title = input("Enter book title: ").strip()
    if not title:
        print("Error: Book title cannot be empty.")
        return

    author_name = input("Enter author name: ").strip()
    if not author_name:
        print("Error: Author name cannot be empty.")
        return

    duplicate = any(
        book.title.casefold() == title.casefold()
        and book.author.casefold() == author_name.casefold()
        for book in library["books"]
    )

    if duplicate:
        confirm = input(
            "A book with this title and author already exists. "
            "Add another copy? (y/n): "
        ).strip().casefold()

        if confirm not in ("y", "yes"):
            print("Book addition cancelled.")
            return

    author = next(
        (
            item for item in library["authors"]
            if item.name.casefold() == author_name.casefold()
        ),
        None,
    )

    if author is None:
        author_id = generate_id(
            [item.to_dict() for item in library["authors"]],
            "author",
        )
        author = Author(author_id, author_name)
        library["authors"].append(author)

    book_id = generate_id(
        [item.to_dict() for item in library["books"]],
        "book",
    )
    book = Book(book_id, title, author.name, available=True)
    library["books"].append(book)

    _save_library_objects(library)

    print("\nBook added successfully!")
    print(book.display_info())


def search_books() -> None:
    """Search books by title or author."""
    library = _load_library_objects()
    term = input("Search by title or author: ").strip().casefold()

    if not term:
        print("Please enter a search term.")
        return

    results = [
        book for book in library["books"]
        if term in book.title.casefold()
        or term in book.author.casefold()
    ]

    if not results:
        print("No matching books found.")
        return

    print("\nSearch Results")
    for book in results:
        print(book.display_info())


def borrow_book() -> None:
    """Record a borrowing and mark the book unavailable."""
    library = _load_library_objects()

    book_number = input("Enter the book number: ").strip()
    book = _find_book(library, book_number)

    if book is None:
        print("Book not found.")
        return

    if not book.available:
        print("This book is already borrowed.")
        return

    borrower_name = input("Enter your full name: ").strip()
    if not borrower_name:
        print("Borrower name cannot be empty.")
        return

    borrower = next(
        (
            item for item in library["borrowers"]
            if item.name.casefold() == borrower_name.casefold()
        ),
        None,
    )

    if borrower is None:
        borrower_id = generate_id(
            [item.to_dict() for item in library["borrowers"]],
            "borrower",
        )
        borrower = Borrower(borrower_id, borrower_name)
        library["borrowers"].append(borrower)

    borrowing = {
        "id": generate_id(library["borrowings"], "borrowing"),
        "book_id": book.id,
        "borrower_id": borrower.id,
        "borrowed_at": datetime.now().strftime("%Y-%m-%d"),
        "returned_at": None,
    }

    book.available = False
    library["borrowings"].append(borrowing)

    _save_library_objects(library)

    print("\nBorrowing successful!")
    print(f"Book: {book.title}")
    print(f"Borrower: {borrower.name}")
    print(f"Borrowing reference: {borrowing['id']}")


def return_book() -> None:
    """Return a book after verifying its active borrowing record."""
    library = _load_library_objects()

    book_number = input("Enter the book number to return: ").strip()
    book = _find_book(library, book_number)

    if book is None:
        print("Book not found.")
        return

    if book.available:
        print("This book is already marked as available.")
        return

    borrower_name = input(
        "Enter the full name of the person who borrowed it: "
    ).strip()

    if not borrower_name:
        print("Borrower name cannot be empty.")
        return

    borrower = next(
        (
            item for item in library["borrowers"]
            if item.name.casefold() == borrower_name.casefold()
        ),
        None,
    )

    if borrower is None:
        print("Borrower not found. Return rejected.")
        return

    borrowing = next(
        (
            record for record in reversed(library["borrowings"])
            if record["book_id"] == book.id
            and record["borrower_id"] == borrower.id
            and record["returned_at"] is None
        ),
        None,
    )

    if borrowing is None:
        print(
            "Return rejected: this borrower does not have "
            "an active borrowing record for this book."
        )
        return

    borrowing["returned_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    book.available = True

    _save_library_objects(library)

    print("\nReturn successful!")
    print(f"Book: {book.title}")
    print(f"Returned by: {borrower.name}")
    print(f"Borrowing reference: {borrowing['id']}")


def show_available_books() -> None:
    """Display all books currently available for borrowing."""
    library = _load_library_objects()
    books = [book for book in library["books"] if book.available]

    print("\nAvailable Books")
    if not books:
        print("No available books.")
        return

    for book in books:
        print(book.display_info())


def show_borrowed_books() -> None:
    """Display all books currently borrowed."""
    library = _load_library_objects()
    books = [book for book in library["books"] if not book.available]

    print("\nBorrowed Books")
    if not books:
        print("No borrowed books.")
        return

    for book in books:
        print(book.display_info())


def show_books_by_author() -> None:
    """Display books written by a specified author."""
    library = _load_library_objects()
    author_name = input("Enter author name: ").strip()

    if not author_name:
        print("Author name cannot be empty.")
        return

    books = [
        book for book in library["books"]
        if book.author.casefold() == author_name.casefold()
    ]

    print(f"\nBooks by {author_name}")
    if not books:
        print("No books found for this author.")
        return

    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(f"{book.id} | {book.title} | {status}")


def show_borrowing_history() -> None:
    """Display borrowing records and their current status."""
    library = _load_library_objects()
    borrowings = library["borrowings"]

    print("\nBORROWING HISTORY")
    if not borrowings:
        print("No borrowing records found.")
        return

    books = {book.id: book for book in library["books"]}
    borrowers = {
        borrower.id: borrower for borrower in library["borrowers"]
    }

    for number, record in enumerate(borrowings, start=1):
        book = books.get(record["book_id"])
        borrower = borrowers.get(record["borrower_id"])

        book_title = book.title if book else "Unknown book"
        book_id = book.id if book else record["book_id"]
        borrower_name = borrower.name if borrower else "Unknown borrower"

        borrowed_at = record.get("borrowed_at") or "Unknown date"
        returned_at = record.get("returned_at")

        if returned_at:
            status = "RETURNED"
        else:
            returned_at = "Not yet returned"
            status = "CURRENTLY BORROWED"

        print(f"\nRecord #{number}")
        print(f"Borrowing ID : {record.get('id', 'N/A')}")
        print(f"Book         : {book_title}")
        print(f"Book ID      : {book_id}")
        print(f"Borrower     : {borrower_name}")
        print(f"Borrowed date: {borrowed_at}")
        print(f"Returned at  : {returned_at}")
        print(f"Status       : {status}")

    returned_count = sum(
        1 for record in borrowings if record.get("returned_at")
    )
    active_count = len(borrowings) - returned_count

    print(f"\nTotal borrowing records: {len(borrowings)}")
    print(f"Books returned         : {returned_count}")
    print(f"Currently borrowed     : {active_count}")
