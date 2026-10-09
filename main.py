
from library_service import (
    add_book,
    search_books,
    borrow_book,
    return_book,
    show_available_books,
    show_borrowed_books,
    show_books_by_author,
    show_borrowing_history,
)


def main():
    actions = {
        "1": add_book,
        "2": search_books,
        "3": show_available_books,
        "4": show_borrowed_books,
        "5": borrow_book,
        "6": return_book,
        "7": show_books_by_author,
        "8": show_borrowing_history,
    }

    while True:
        print("\n      LIBRARY INVENTORY   ")
        print("1. Add a book")
        print("2. Search books")
        print("3. Show available books")
        print("4. Show borrowed books")
        print("5. Borrow a book")
        print("6. Return a book")
        print("7. Show books by author")
        print("8. Show borrowing history")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "9":
            print("Thank you for using the Library Inventory!")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid choice. Please enter a number from 1 to 9.")
            continue

        try:
            action()
        except (OSError, ValueError) as error:
            print(f"Operation could not be completed: {error}")


if __name__ == "__main__":
    main()
