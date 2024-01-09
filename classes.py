import datetime
import psycopg2
from typing import List
from setup_tables import Db_books_review

class Review:
    sno: int
    name: str
    reviewer: str
    rating: int
    description: str
    js_verified: str
    date: datetime.datetime
    timestamp: str
    asin: int
    
    def _init_ (self,
                  sno: int,
                  name: str,
                  reviewer: str,
                  rating: int,
                  description: str,
                  js_verified: str,
                  date: datetime.datetime,
                  timestamp: str,
                  asin: int):
        
        self.sno = sno
        self.name = name
        self.reviewer = reviewer
        self.rating = rating
        self.description = description
        self.js_verified = js_verified 
        self.date = date 
        self.timestamp = timestamp 
        self.asin = asin

class Book:
    rank: float
    title:str
    price: float
    rating: float
    author: str
    year_of_publication: datetime.datetime
    genre: str
    url: str
    reviews: list[Review]
 
    def _init_(self,
                 rank: float,
                 title:str,
                 price: float,
                 rating: float,
                 author: str,
                 year_of_publication: datetime.datetime,
                 genre: str,
                 url: str,
                 ):
        
        self.rank = rank
        self.title = title
        self.price = price
        self.rating = rating
        self.author = author
        self.year_of_publication = year_of_publication
        self.genre = genre
        self.url = url
        self.reviews =  []
    
    def _str_(self) -> str:
        return f'{self.author}'
        
    def add_review(self, review):
        self.reviews.append(review)
        
    def average_rating(self) -> float:
        sum = 0
        for review in self.reviews:
            sum += review.rating
        return sum / len(self.reviews)

    def get_review_count(self) -> int:
        return len(self.reviews)
        
def print_book(book : Book):
    print(f'{book.author}')
    
        
def load_books() -> List[Book]:
    conn = psycopg2.connect(
    dbname='postgres', user='postgres', password='1234', host='localhost', port='5432'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books_data = cursor.fetchall()
    books = []
    for book_data in books_data:
        rank,title,price,rating,author,year_of_publication,genre,url= book_data
        book = Book(rank,title,price,rating,author,year_of_publication,genre,url)
        print(book)
        cursor.execute("SELECT sno, name, reviewer, rating, description, js_verified, date, timestamp, asin FROM reviews WHERE book_name = %s", (title,))
        reviews_data = cursor.fetchall()
        for review_data in reviews_data:
            sno = review_data[0]
            name = review_data[2]
            reviewer = review_data[3]
            rating = review_data[4]
            description = review_data[5]
            js_verified = review_data[6]
            date = review_data[7]
            timestamp = review_data[8]
            asin = review_data[9]  
            book.add_review(Review(sno,name,reviewer,rating,description,js_verified,date,timestamp,asin))
        books.append(book)

    conn.close()

    return books

def count_books(books_with_reviews):
    return len(books_with_reviews)

def count_first_book_reviews_not_oop(books_with_reviews: list[Book]):
    return len(books_with_reviews[0].reviews)

def count_first_book_reviews(books_with_reviews: list[Book]):
    return books_with_reviews[0].get_review_count()

# ilosc recenzji pierwszej ksiazki na lisscie

books_with_reviews = load_books()

how_many = count_books(books_with_reviews)
print(how_many)

first_book_review_count = count_first_book_reviews(books_with_reviews)
print(first_book_review_count)