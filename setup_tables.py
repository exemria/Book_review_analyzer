import psycopg2
import csv

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
    cur.execute("""CREATE TABLE books (
        rank VARCHAR(50),
        book_title VARCHAR(50),
        book_price VARCHAR(50),
        rating INTEGER,
        author VARCHAR(50),
        year_of_publication INTEGER,
        genre VARCHAR(50),
        url VARCHAR(100)
    )
    """)
    
    
    

def insert_data_from_csv(cur, file_url):
    with open (file_url, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        next(reader)
        #cur.copy_from(csvfile,books,sep=',')
        for row in reader:
            cur.execute("""INSERT INTO books (rank,book_title,book_price,rating,author,year_of_publication,genre,url)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",row)
            

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
        csv_file_url = r'C:\Users\konra\Desktop\Python\programmes\SQL-projects\Top_100_Trending_Books.csv'
        create_table_books(cur)
    except Exception as e:
        print("Error no table created", e)

    try:
        insert_data_from_csv(cur, csv_file_url)
    except Exception as e:
        print("Error inserting data from csv", e)
    
    conn.commit()
    cur.close()
    conn.close()

