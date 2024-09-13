# Directory Manager

## Description

This project demonstrates directory management with the ability to create folders at various levels of nesting. The program includes functions for creating new folders, adding folders, and displaying the directory structure in a readable format. Functionality is verified using `pytest` tests.

## Project Structure
```bash
    directory-manager/
      │
      ├── run.py                   # Script to run the program
      │
      ├── requirements.txt         # Contains all the dependency packages
      │
      ├── services/                # Contains implementation of classes
      │   ├── __init__.py          # Initializes the package
      │   ├── directory_manager.py # Implementation of DirectoryManager class
      │   └── file_manager.py      # Implementation of FileManager class
      │
      └── tests/                  # Contains tests 
          ├── __init__.py         # Initializes the package
          └── test_directory_manager.py # Tests for DirectoryManager

```
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/oWlogona/BackendCodingChallenge15.git
    cd directory-manager
    ```

2. Create and activate a virtual environment (optional):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Program

To run the program, use the `run.py` file. Currently, the program does not have a CLI (Command Line Interface), so functionality is tested through the provided tests.

### Running Tests

To run tests, use `pytest`. This will ensure that your code's functionality is verified.

```bash
pytest
