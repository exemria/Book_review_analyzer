import csv
import psycopg2
from datetime import datetime
from setup_tables import *

def books_data_dict(self, file_path1) -> dict: 
    books_data = {}
    with open(file_path1, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row = [None if cell == '' else cell for cell in row]
            book_title = row[1]
            books_data[book_title] = row
            
        return books_data
    
def insert_books_data(self, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                row = [None if cell == '' else cell for cell in row]
                self.insert_book(row)
    except psycopg2.IntegrityError as e:
        if 'duplicate key value violates unique constraint "books_pkey"' in str(e):
            print("Duplicate book_title found. Handling duplicate...")
        else:
            print("Error inserting data into the books table:", e)

def insert_book(self, book_data):
    try:
        self.cur.execute("""
            INSERT INTO books (rank, book_title, book_price, rating, author, year_of_publication, genre, url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, book_data)
        self.conn.commit()
    except Exception as e:
        print(f"Error inserting book {book_data}: {e}")

    

def insert_review_data(self, file_path):
    books_dict = books_data_dict()

    with open(file_path, 'r', encoding='utf-8') as reviews_csv:
        reviews_reader = csv.reader(reviews_csv)
        next(reviews_reader)

        for review_row in reviews_reader:
            book_name = review_row[1]

            if book_name in books_dict:
                review_data = preprocess_review_data(review_row)
                self.insert_review(review_data)

def preprocess_review_data(review_row):
    date_str = review_row[7]
    try:
        date_numeric = datetime.strptime(date_str, '%d-%m-%Y').timestamp()
    except ValueError:
        date_numeric = None
    review_row[7] = date_numeric
    return review_row

def insert_review(self, review_data):
    try:
        self.cur.execute("""
            INSERT INTO reviews (Sno, book_name, review_title, reviewer, rating,
                                review_description, js_verified, date, timestamp, ASIN)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, review_data)
        self.conn.commit()
    except Exception as e:
        print(f"Error inserting review {review_data}: {e}")
