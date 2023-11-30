import psycopg2
import csv
from datetime import datetime

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
            FOREIGN KEY ("book_name") REFERENCES "books"("book_title")
    ''')
    
    
    

def insert_data_from_csv(cur, file_path1, file_path2):
    with open (file_path1, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        #cur.copy_from(csvfile,books,sep=',')
        for row in reader:
            row = [None if cell == '' else cell for cell in row]
            #year_of_publication = row[5] if row[5] != '' else 0 # Handle empty string
            ## Convert empty strings to None 
            #row[5] = float(year_of_publication) if year_of_publication is not 0 else 0
            cur.execute("""INSERT INTO books (rank,book_title,book_price,rating,author,year_of_publication,genre,url)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",row)
            
    with open (file_path2, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        #cur.copy_from(csvfile,books,sep=',')
        for row in reader:
            row = [None if cell == '' else cell for cell in row]
             # Convert date string to a numeric representation (e.g., timestamp)
            date_str = row[7]  # Assuming date is at index 7
            try:
                date_numeric = datetime.strptime(date_str, '%d-%m-%Y').timestamp()  # Convert date to timestamp
            except ValueError:
                date_numeric = None  # Handle invalid date format

            # Replace date string with numeric representation
            row[7] = date_numeric
            #book_name = row[1]
            #cur.execute(" SELECT book_title FROM books WHERE book_title = %s", (book_name,))
            #cur.fetchone()
                    

            cur.execute("""INSERT INTO reviews (Sno,book_name,review_title,reviewer,rating,review_description,js_verified,date,timestamp,ASIN)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",row)
            

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
        csv_file_books_path = r'C:\Users\konra\Desktop\Python\programmes\SQL-projects\Top_100_Trending_Books.csv'
        csv_file_reviews_path = r'C:\Users\konra\Desktop\Python\programmes\SQL-projects\customer_reviews.csv'
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
