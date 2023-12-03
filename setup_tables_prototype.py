import psycopg2
import csv
from datetime import datetime
import os



def connect_to_database():
    return psycopg2.connect(
        dbname = "amazon",
        user = "postgres",
        password = "5329",
        host = "localhost",
        port = "5432"
    )
    

# download all tables from database amazon if exists
def get_table_list(cur):
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    return cur.fetchall()

def drop_all_tables(cur,tables):
    for table in tables:
        cur.execute(f" DROP TABLE IF EXISTS {table[0]} CASCADE")
    

def update_books_data(cur):

    cur.execute("SELECT book_title FROM books WHERE book_title = %s", (book_title,))
    existing_record = cur.fetchone()

    if existing_record:
        print("Book already exists. Updating information or skipping insertion...")
    # Handle the case where the book already exists
    # For example, you might want to update some information:
    # You can fetch the existing data and decide how to proceed:
        cur.execute("SELECT * FROM books WHERE book_title = %s", (book_title,))
        existing_book_data = cur.fetchone()

    # Assuming you want to update the book's rating and author information:
    # new_rating = ...
    # new_author = ...
    # Then perform an UPDATE query:
    # cur.execute("UPDATE books SET rating = %s, author = %s WHERE book_title = %s", (new_rating, new_author, book_title))

    # Alternatively, you might want to skip the insertion entirely:
    # return or continue depending on your logic
    else:
        print("Inserting a new book...")
    # Insert the new record
    # ...
# create table from csv file

def create_table_books(cur):
    cur.execute('''
        CREATE TABLE "books" (
        "rank" FLOAT,
        "book_title" VARCHAR(255) PRIMARY KEY,
        "book_price" VARCHAR(255),
        "rating" FLOAT,
        "author" VARCHAR(255),
        "year_of_publication" TEXT,
        "genre" VARCHAR(255),
        "url" VARCHAR(255)
    )
    ''')

def create_table_reviews(cur):
    cur.execute('''
        CREATE TABLE "reviews" (
            "sno" FLOAT PRIMARY KEY,
            "book_name" VARCHAR(255),
            "review_title" VARCHAR(255),
            "reviewer" VARCHAR(255),
            "rating" FLOAT,
            "review_description" TEXT,
            "js_verified" VARCHAR(255), 
            "date" NUMERIC, 
            "timestamp" VARCHAR(255), 
            "asin" VARCHAR(255),
        FOREIGN KEY ("book_name") REFERENCES "books"("book_title"))
    ''')
    
    #--FOREIGN KEY ("book_name") REFERENCES "books"("book_title")--
    

def insert_data_from_csv(cur, file_path1, file_path2):
    with open(file_path1, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row = [None if cell == '' else cell for cell in row]
            book_title = row[1]

            cur.execute("SELECT book_title FROM books WHERE book_title = %s", (book_title,))
            existing_record = cur.fetchone()

            if existing_record:
                # Book exists in the books table, proceed with insertion into reviews table
                with open(file_path2, 'r', encoding='utf-8') as reviews_csv:
                    reviews_reader = csv.reader(reviews_csv)
                    next(reviews_reader)
                    for review_row in reviews_reader:
                        # Assuming the book_name is in index 1 of the reviews CSV
                        if review_row[1] == book_title:
                            # Convert date string to a numeric representation (e.g., timestamp)
                            date_str = review_row[7]  # Assuming date is at index 7
                            try:
                                date_numeric = datetime.strptime(date_str, '%d-%m-%Y').timestamp()
                            except ValueError:
                                date_numeric = None

                            review_row[7] = date_numeric

                            cur.execute("""
                                INSERT INTO reviews (Sno, book_name, review_title, reviewer, rating,
                                                    review_description, js_verified, date, timestamp, ASIN)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """, review_row)
            else:
                print(f"Book '{book_title}' does not exist in the 'books' table. Skipping insertion into 'reviews'.")

                    
            

def main():
    try:

        conn = connect_to_database()
        cur = conn.cursor()
    except Exception as e:
        print("Error not connected to database", e)
    try:
        tables = get_table_list(cur)

        drop_all_tables(cur,tables)
    except Exception as e:
        print("Error dropping tables:", e)
    
    try:
        absolute_path = os.path.dirname(__file__)
        relative_path_to_bookscsv = "resources\Top_100_Trending_Books.csv"
        relative_path_to_reiewscsv = "resources\customer_reviews.csv"
        csv_file_books_path = os.path.join(absolute_path, relative_path_to_bookscsv)
        csv_file_reviews_path = os.path.join(absolute_path, relative_path_to_reiewscsv)
        #csv_file_books_path = os.path.join(os.path.dirname(__file__), "Top_100_Trending_Books.csv")
        #csv_file_reviews_path = os.path.join(os.path.dirname(__file__), "customer_reviews.csv")
        #csv_file_books_path = r"C:\Users\konra\Desktop\Python\programmes\SQL-projects\resources\Top_100_Trending_Books.csv" # relative path zrob folder resoursed 
        #csv_file_reviews_path = r"C:\Users\konra\Desktop\Python\programmes\SQL-projects\resources\customer_reviews.csv" # bibliotego OS find path 
        cur.execute('DROP TABLE IF EXISTS "books" CASCADE')
        create_table_books(cur)
        create_table_reviews(cur)
    except Exception as e:
        print("Error no table created", e)

    try:
        insert_data_from_csv(cur, csv_file_books_path, csv_file_reviews_path)

    except Exception as e:
        print("Error inserting data from csv", e)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
