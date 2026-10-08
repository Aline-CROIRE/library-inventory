from book import Book, EBook, AudioBook
from borrower import Borrower
from author import Author


def main():
    book = Book(
        "BK001",
        "Things Fall Apart",
        "Chinua Achebe"
    )

    ebook = EBook(
        "EB001",
        "Python Basics",
        "AmaliTech",
        5.2
    )

    audiobook = AudioBook(
        "AB001",
        "The River Between",
        "Ngugi wa Thiong'o",
        420
    )

    borrower = Borrower(
        "BR001",
        "Test Borrower"
    )

    author = Author(
        "AU001",
        "Chinua Achebe"
    )

    print("\n--- Library Resources ---")
    print(book)
    print(book.display_info())

    print(ebook.display_info())
    print(audiobook.display_info())

    print("\n--- Borrower ---")
    print(borrower)

    print("\n--- Author ---")
    print(author)


if __name__ == "__main__":
    main()