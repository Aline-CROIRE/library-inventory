import json

def add_book():
    book_id=input("Enter book ID: ")
    title=input("Enter book title: ")
    author=input("Enter book author: ")

    with open("data/library.json","r") as file:
        library=json.load(file)
        for book in library["books"]:
            if book["id"]==book_id:
                print(f"Book with ID '{book_id}' already exists in the library.")
                return

    book= {
        "id": book_id,
        "title": title,
        "author": author,
        "available": True

    }

    
    library["books"].append(book)
    with open("data/library.json","w") as file:
        json.dump(library, file, indent=4)
    
    print(f"Book '{title}' by {author} added to the library Successfully !")


def search_book():
    search_term=input("Enter book title or author to search: ")
    with open("data/library.json","r") as file:
        library=json.load(file)
        result=[
            book
            for book in library["books"]
            if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()
        ]
        

        
        if result:
            print("Found books:")
            for book in result:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Available: {book['available']}")
        else:
            print("No books found.")


def show_available_books():
    with open("data/library.json","r") as file:
        library=json.load(file)
        available_books=[
            book
            for book in library["books"]
            if book["available"]
        ]
        
        if available_books:
            print("Available books:")
            for book in available_books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}")
        else:
            print("No available books.")

def show_borrowed_books():
    with open("data/library.json","r") as file:
        library=json.load(file)
        borrowed_books=[
            book
            for book in library["books"]
            if not book["available"]
        ]
        
        if borrowed_books:
            print("Borrowed books:")
            for book in borrowed_books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}")
        else:
            print("No borrowed books.")


def borrow_book():
    book_id=input("Enter book ID to borrow: ")
    with open("data/library.json","r") as file:
        library=json.load(file)
        for book in library["books"]:
            if book["id"]==book_id:
                if book["available"]:
                    book["available"]=False
                    with open("data/library.json","w") as file:
                        json.dump(library, file, indent=4)
                    print(f"You have borrowed '{book['title']}' by {book['author']}.")
                    return
                else:
                    print(f"Book '{book['title']}' is currently not available.")
                    return
        print(f"No book found with ID '{book_id}'.")


def return_book():
    book_id=input("Enter book ID to return: ")
    with open("data/library.json","r") as file:
        library=json.load(file)
        for book in library["books"]:
            if book["id"]==book_id:
                if not book["available"]:
                    book["available"]=True
                    with open("data/library.json","w") as file:
                        json.dump(library, file, indent=4)
                    print(f"You have returned '{book['title']}' by {book['author']}.")
                    return
                else:
                    print(f"Book '{book['title']}' was not borrowed.")
                    return
        print(f"No book found with ID '{book_id}'.")

    
return_book()