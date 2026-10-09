# Library Inventory Management System

## Overview

The Library Inventory Management System is a Python command-line application for managing books and tracking borrowing and returns. It demonstrates Python fundamentals, object-oriented programming, modular design, file handling, data validation, and JSON persistence.

## Features

- **Book management:** Add books and generate unique book IDs automatically.
- **Book search:** Search for books by title or author.
- **Availability tracking:** View available and borrowed books.
- **Borrowing management:** Record borrowing transactions and prevent a book from being borrowed when it is unavailable.
- **Book returns:** Validate the active borrowing record before accepting a return.
- **Borrowing history:** View borrowing transactions, borrower details, dates, return status, and return timestamps.
- **Author management:** Register authors and reuse existing author records.
- **Data persistence:** Store library records in a JSON file so that data remains available after restarting the application.
- **Input validation:** Handle invalid menu choices and validate required information.

## Technologies Used

- Python 
- JSON for data storage
- Python standard library
- Object-oriented programming (OOP)

## Project Structure

```text
library-inventory/
├── main.py
├── library_service.py
├── utils.py
├── library_resource.py
├── book.py
├── author.py
├── borrower.py
├── data/
│   └── library.json
└── README.md
```

### Module Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Displays the menu and dispatches user choices. |
| `library_service.py` | Implements book management, borrowing, returning, searching, and reporting operations. |
| `utils.py` | Handles JSON persistence and automatic ID generation. |
| `library_resource.py` | Defines the abstract base class for library resources. |
| `book.py` | Defines book classes and their behaviors. |
| `author.py` | Defines the author model. |
| `borrower.py` | Defines the borrower model. |
| `data/library.json` | Stores book, author, borrower, and borrowing records. |

## Requirements

- Python 3 installed on your computer.
- A terminal or command prompt.

The application uses Python's standard library and does not require third-party packages for its core functionality.

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Aline-CROIRE/library-inventory.git
   ```

2. Navigate to the project directory:

   ```bash
   cd library-inventory
   ```

3. Confirm that `data/library.json` exists and contains valid JSON.

## Running the Application

Run the following command from the project root:

```bash
python main.py
```

The application displays a menu for performing library operations. Select the desired option and follow the prompts.

## Data Storage

The application stores records in `data/library.json`.

The JSON data includes:

- Books and their availability.
- Author records.
- Borrower records.
- Borrowing transactions, including borrowing dates and return information.

Changes are saved to the JSON file so records can persist between application sessions.

## Validation and Business Rules

The application applies validation rules to help maintain consistent records:

- Book titles, author names, and borrower names cannot be empty.
- Book identifiers are generated automatically.
- Unavailable books cannot be borrowed again.
- A return must match an active borrowing record for the selected book and borrower.
- A completed borrowing transaction retains its history.
- Invalid menu choices are rejected.

## Object-Oriented Programming Concepts

The project demonstrates:

- **Abstraction:** An abstract base class defines a common interface for library resources.
- **Inheritance:** Book-related classes reuse shared behavior.
- **Polymorphism:** Resource classes can provide their own implementations of `display_info()`.
- **Encapsulation:** Classes group related data and behavior.
- **Special methods:** Methods such as `__repr__()` and `__eq__()` provide object representations and equality comparisons.
- **Modularity:** Application responsibilities are separated into dedicated Python modules.

## Manual Verification

The application was checked using borrowing and returning scenarios, including:

- Adding a book and checking its generated ID.
- Borrowing an available book.
- Rejecting a second borrowing of an unavailable book.
- Rejecting a return by an incorrect borrower.
- Accepting a valid return.
- Checking borrowing history and saved records.

## Future Improvements

- Add a graphical user interface or web interface.
- Introduce authenticated borrower accounts and unique library-card numbers.
- Add due dates, overdue notifications, and fine calculations.
- Use a database for more robust storage and concurrent access.
- Expand automated tests as the application grows.

## Author

**Aline NIYONIZERA**

GitHub: [Aline-CROIRE](https://github.com/Aline-CROIRE)

