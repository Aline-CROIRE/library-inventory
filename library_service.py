
from datetime import datetime

from utils import load_library, save_library, generate_id


def _find_book(library, user_input):
    """Find a book by its displayed number or full ID."""
    value = user_input.strip()

    if value.isdigit():
        number = int(value)
        book_id = f"BK{number:03d}"
    else:
        book_id = value

    return next(
        (book for book in library["books"] if book["id"] == book_id),
        None,
    )


def add_book():
    library = load_library()

    title = input("Enter book title: ").strip()
    if not title:
        print("Book title cannot be empty.")
        return

    author_name = input("Enter author name: ").strip()
    if not author_name:
        print("Author name cannot be empty.")
        return

    book_id = generate_id(library["books"], "book")

   
    author = next(
        (
            item for item in library["authors"]
            if item["name"].casefold() == author_name.casefold()
        ),
        None,
    )

    if author is None:
        author_id = generate_id(library["authors"], "author")
        library["authors"].append({
            "id": author_id,
            "name": author_name,
        })

    library["books"].append({
        "id": book_id,
        "title": title,
        "author": author_name,
        "available": True,
    })

    
    print(f"Book added successfully! Its number is {book_id}.")


def search_books():
    library = load_library()
    term = input("Search by title or author: ").strip().casefold()

    if not term:
        print("Please enter a search term.")
        return

    results = [
        book for book in library["books"]
        if term in book["title"].casefold()
        or term in book["author"].casefold()
    ]

    if not results:
        print("No matching books found.")
        return

    print("\n    Search Results  ")
    for book in results:
        status = "Available" if book["available"] else "Borrowed"
        print(
            f"{book['id']} | {book['title']} | "
            f"{book['author']} | {status}"
        )


def borrow_book():
    library = load_library()
    book_number = input("Enter the book number: ").strip()

    book = _find_book(library, book_number)

    if book is None:
        print("Book not found. Please check the book number.")
        return

    if not book["available"]:
        print("That book is already borrowed.")
        return

    borrower_name = input("Enter borrower name: ").strip()

    if not borrower_name:
        print("Borrower name cannot be empty.")
        return

    borrower = next(
        (
            item for item in library["borrowers"]
            if item["name"].casefold() == borrower_name.casefold()
        ),
        None,
    )

    if borrower is None:
        borrower_id = generate_id(library["borrowers"], "borrower")
        borrower = {
            "id": borrower_id,
            "name": borrower_name,
        }
        library["borrowers"].append(borrower)

    borrowing_id = generate_id(library["borrowings"], "borrowing")

    library["borrowings"].append({
        "id": borrowing_id,
        "book_id": book["id"],
        "borrower_id": borrower["id"],
        "borrowed_at": datetime.now().isoformat(timespec="seconds"),
        "returned_at": None,
    })

    book["available"] = False
    save_library(library)

    print(
        f"'{book['title']}' borrowed successfully by "
        f"{borrower['name']}."
    )


def return_book():
    library = load_library()
    book_number = input("Enter the book number to return: ").strip()

    book = _find_book(library, book_number)

    if book is None:
        print("Book not found. Please check the book number.")
        return

    if book["available"]:
        print("That book is already available.")
        return

   
    borrowing = next(
        (
            record for record in reversed(library["borrowings"])
            if record["book_id"] == book["id"]
            and record["returned_at"] is None
        ),
        None,
    )

    if borrowing is None:
        print("No active borrowing record was found. Data was not changed.")
        return

    borrowing["returned_at"] = datetime.now().isoformat(timespec="seconds")
    book["available"] = True
    save_library(library)

    print(f"'{book['title']}' has been returned successfully.")


def show_available_books():
    library = load_library()
    books = [
        book for book in library["books"]
        if book["available"]
    ]

    print("\n--- Available Books ---")
    if not books:
        print("No available books.")
        return

    for book in books:
        print(f"{book['id']} | {book['title']} | {book['author']}")


def show_borrowed_books():
    library = load_library()
    books = [
        book for book in library["books"]
        if not book["available"]
    ]

    print("\n  Borrowed Books   ")
    if not books:
        print("No borrowed books.")
        return

    for book in books:
        print(f"{book['id']} | {book['title']} | {book['author']}")


def show_books_by_author():
    library = load_library()
    author_name = input("Enter author name: ").strip()

    if not author_name:
        print("Author name cannot be empty.")
        return

    books = [
        book for book in library["books"]
        if book["author"].casefold() == author_name.casefold()
    ]

    print(f"\n    Books by {author_name}    ")
    if not books:
        print("No books found for this author.")
        return

    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(f"{book['id']} | {book['title']} | {status}")


def show_borrowing_history():
    library = load_library()

    print("\n  Borrowing History   ")
    if not library["borrowings"]:
        print("No borrowing history found.")
        return

    borrowers = {
        item["id"]: item["name"]
        for item in library["borrowers"]
    }
    books = {
        item["id"]: item["title"]
        for item in library["books"]
    }

    for record in library["borrowings"]:
        book_title = books.get(record["book_id"], "Unknown book")
        borrower_name = borrowers.get(
            record["borrower_id"], "Unknown borrower"
        )
        status = (
            "Returned" if record["returned_at"] else "Currently borrowed"
        )

        print(
            f"{record['id']} | {book_title} | {borrower_name} | "
            f"Borrowed: {record['borrowed_at']} | {status}"
        )
