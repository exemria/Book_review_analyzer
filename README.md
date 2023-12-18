# SQL-projects# Book Review Analyzer


- Martyna Buczek
- email: mbuczek.dev@gmail.com
- phone_number: +48 784 408 800


### BOOK REVIEW ANALYZER ###

### About the code
This program is a Python-based application designed to interact with a PostgreSQL database containing book-related data sourced from a provided dataset. It's structured in stages to build a functional environment, develop classes representing Books and Reviews, implement methods to perform various data operations, and validate their correctness using unit tests.

### Technologies used

- Python 3.10+: Core programming language. Used standard libraries such as csv, datetime, os, and sys.
- PostgreSQL: Database management system for data storage and retrieval.
- Third-party Libraries:
    - psycopg2: PostgreSQL adapter for the Python programming language used for establishing connection to PostgreSQL databases
    - pytest: Module for writing and running tests

       
### Requirements

- python 3.10 or higher
- PostgreSQL
- dependencies

To install the necessary dependencies, run:
`pip install -r requirements.txt`

### Usage

The CLI supports multiple actions, accessible via commands:

## Login


## Actions


### Structure

- app.py: Main script contains classes for actions
- setup_tables.py: Manages PostgreSQL database operations