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
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
        rank VARCHAR(50),
        book title VARCHAR(50),
        book price VARCHAR(50),
        rating INTEGER,
        author VARCHAR(50),
        year of publication INTEGER,
        genre VARCHAR(50),
        url VARCHAR(100),
    )
    """)
    

def insert_data_from_csv(cur, file_url):
    with open (file_url, 'r', newline ='', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        next(reader)
        for row in reader:
            cur.execute("""INSERT INTO books (
                rank,
                book title,
                book price,
                rating,
                author,
                year of publication,
                genre,
                url )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """,row)






def main():
    
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        tables = get_table_list(cur)

        drop_all_tables(cur,tables)
    except Exception:
        print("Something wrong")
    
    try:
        csv_file_url = r'C:\Users\konra\Desktop\Top-100 Trending Books.csv'
        create_table_books(cur)
    except Exception:
        print("no table created")

    try:
        insert_data_from_csv(cur, csv_file_url)
    except Exception:
        print("problem with inserting data from csv")
    conn.commit()

    cur.close()
    conn.close()

