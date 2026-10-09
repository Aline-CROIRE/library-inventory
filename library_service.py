
from datetime import datetime

from utils import load_library, save_library, generate_id



def add_book():
    print("\n  Add a New Book  ")

    try:
        library = load_library()

        title = input("Enter book title: ").strip()
        if not title:
            print("Error: Book title cannot be empty.")
            return

        author_name = input("Enter author name: ").strip()
        if not author_name:
            print("Error: Author name cannot be empty.")
            return

        
        duplicate = any(
            book["title"].strip().casefold() == title.casefold()
            and book["author"].strip().casefold()
            == author_name.casefold()
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

        book_id = generate_id(library["books"], "book")

        author_exists = any(
            author["name"].strip().casefold()
            == author_name.casefold()
            for author in library["authors"]
        )

        if not author_exists:
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

        save_library(library)

        print("\nBook added successfully!")
        print(f"ID: {book_id}")
        print(f"Title: {title}")
        print(f"Author: {author_name}")
        print("Status: Available")

    except (OSError, ValueError, KeyError) as error:
        print(f"Could not add the book: {error}")


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
        print("Book not found.")
        return

    if not book["available"]:
        print("This book is already borrowed.")
        return

    borrower_name = input("Enter your full name: ").strip()

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
        borrower = {
            "id": generate_id(library["borrowers"], "borrower"),
            "name": borrower_name,
        }
        library["borrowers"].append(borrower)

    borrowing = {
        "id": generate_id(library["borrowings"], "borrowing"),
        "book_id": book["id"],
        "borrower_id": borrower["id"],
        "borrowed_at": datetime.now().strftime("%Y-%m-%d"),
        "returned_at": None,
    }

    book["available"] = False
    library["borrowings"].append(borrowing)

    save_library(library)

    print("\nBorrowing successful!")
    print(f"Book: {book['title']}")
    print(f"Borrower: {borrower['name']}")
    print(f"Borrowing reference: {borrowing['id']}")

def return_book():
    library = load_library()

    book_number = input("Enter the book number to return: ").strip()
    book = _find_book(library, book_number)

    if book is None:
        print("Book not found.")
        return

    if book["available"]:
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
            if item["name"].casefold() == borrower_name.casefold()
        ),
        None,
    )

    if borrower is None:
        print("Borrower not found. Return rejected.")
        return

    borrowing = next(
        (
            record for record in reversed(library["borrowings"])
            if record["book_id"] == book["id"]
            and record["borrower_id"] == borrower["id"]
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

    borrowing["returned_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    book["available"] = True

    save_library(library)

    print("\nReturn successful!")
    print(f"Book: {book['title']}")
    print(f"Returned by: {borrower['name']}")
    print(f"Borrowing reference: {borrowing['id']}")


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

        borrowed_at = datetime.fromisoformat(
            record["borrowed_at"]
        ).strftime("%Y-%m-%d")

        if record.get("returned_at"):
            returned_at = datetime.fromisoformat(
                record["returned_at"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            status = "Returned"
        else:
            returned_at = "Not yet returned"
            status = "Currently borrowed"

        
        print(f"Book: {book_title}")
        print(f"Borrower: {borrower_name}")
        print(f"Borrowed date: {borrowed_at}")
        print(f"Returned at: {returned_at}")
        print(f"Status: {status}")


def show_borrowing_history():
    library = load_library()

   
    print("    BORROWING HISTORY  ")
  

    borrowings = library["borrowings"]

    if not borrowings:
        print("No borrowing records found.")
        return

    borrowers = {
        borrower["id"]: borrower["name"]
        for borrower in library["borrowers"]
    }

    books = {
        book["id"]: book
        for book in library["books"]
    }

    for number, record in enumerate(borrowings, start=1):
        book = books.get(record["book_id"])
        book_title = book["title"] if book else "Unknown book"
        book_id = book["id"] if book else record["book_id"]

        borrower_name = borrowers.get(
            record["borrower_id"], "Unknown borrower"
        )

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


    print(f"Total borrowing records: {len(borrowings)}")

    returned_count = sum(
        1 for record in borrowings if record.get("returned_at")
    )
    active_count = len(borrowings) - returned_count

    print(f"Books returned         : {returned_count}")
    print(f"Currently borrowed     : {active_count}")

