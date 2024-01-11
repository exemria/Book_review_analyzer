from datetime import datetime
import psycopg2
from typing import List

class Review:
    sno: int
    name: str
    reviewer: str
    rating: float
    description: str
    js_verified: str
    date: datetime
    timestamp: str
    asin: int
    
    def __init__ (self,
                  sno: int,
                  name: str,
                  reviewer: str,
                  rating: float,
                  description: str,
                  js_verified: str,
                  date: datetime,
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
    year_of_publication: datetime
    genre: str
    url: str
    reviews: list[Review]
 
    def __init__(self,
                 rank: float,
                 title:str,
                 price: float,
                 rating: float,
                 author: str,
                 year_of_publication: datetime,
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
    
    def __str__(self) -> str:
        return (f'{self.author}')
        #,self.rank = rank
        #self.title = title
        #self.price = price
        #self.rating = rating
        #self.author = author
        #self.year_of_publication = year_of_publication
        #self.genre = genre
        #self.url = url
        #self.reviews'
        
    def add_review(self, review):
        self.reviews.append(review)
        
    def average_rating(self) -> float:
        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews) if self.reviews else 0.0

    def get_review_count(self) -> int:
        return len(self.reviews)
    
def load_books() -> List[Book]:
    conn = psycopg2.connect(dbname='amazon', user='postgres', password='5329', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books_data = cursor.fetchall()
    books = []
    for book_data in books_data:
        rank = book_data[0]
        title = book_data[1]
        price = float(book_data[2])
        rating = book_data[3]
        author = book_data[4]
        year_of_publication = book_data[5]
        genre = book_data[6]
        url = book_data[7]
        book = Book(rank,title,price,rating,author,year_of_publication,genre,url)
        print(book)
        cursor.execute("SELECT sno, review_title, reviewer, rating, review_description, js_verified, date, timestamp, asin FROM reviews WHERE book_name = %s", (title,))
        reviews_data = cursor.fetchall()
        for review_data in reviews_data:
            sno = review_data[0]
            name = review_data[1]
            reviewer = review_data[2]
            rating = review_data[3]
            description = review_data[4]
            js_verified = review_data[5]
            date = review_data[6]
            timestamp = review_data[7]
            asin = review_data[8] 
            book.add_review(Review(sno,name,reviewer,rating,description,js_verified,date,timestamp,asin))
        books.append(book)

    conn.close()

    return books

def count_books(books_with_reviews: list[Book]):
    return len(books_with_reviews)

def count_first_book_reviews_not_oop(books_with_reviews: list[Book]):
    return len(books_with_reviews[0].reviews)

def count_first_book_reviews(books_with_reviews: list[Book]):
    return books_with_reviews[0].get_review_count()

def avarage_book_price(books_with_reviews: list[Book]):
    total_price = sum(book.price for book in books_with_reviews)
    avarage_price = total_price / len(books_with_reviews) if books_with_reviews else 0.0
    return avarage_price

def print_reviews_for_book(books: List[Book]):
    found = False
    for book in books:
        found = True
        print(f"Reviews for '{book.title}':")
        for index, review in enumerate(book.reviews, start=1):
            print(f"Review {index}:")
            print(f"Sno: {review.sno}")
            print(f"Name: {review.name}")
            print(f"Reviewer: {review.reviewer}")
            print(f"Rating: {review.rating}")
            print(f"Description: {review.description}")
            print(f"js_verified: {review.js_verified}")
            print(f"timestamp: {review.timestamp}")
            print(f"asin: {review.asin}")

            print("==============================")
    if not found:
        print("No books found.")

def best_worst_rating_book(books_with_reviews: list[Book]) ->tuple:
    reviews = [review for book in books_with_reviews for review in book.reviews]
    max_review = max(reviews, key=lambda review: review.rating, default=None)
    min_review = min(reviews, key=lambda review: review.rating)

    max_rating = max_review.rating if max_review else 0
    min_rating = min_review.rating if min_review else 0

    max_author = next((book.author for book in books_with_reviews if max_review in book.reviews), None)
    min_author = next((book.author for book in books_with_reviews if min_review in book.reviews), None)

    return (max_rating, max_author), (min_rating, min_author)

#Znajdź autorów, którzy mają na tej liście więcej niż 1 książkę oraz podaj ich wraz z
#liczbą ich książek na liście w kolejności od największej ilości książek. Gdyby było ich
#dużo ogranicz się do 5 autorów o największej ilości książek
# def how_many_autors_books(books_with_reviews):
# if booktitle >1: return author

books_with_reviews = load_books()

how_many = count_books(books_with_reviews)
print(how_many)

first_book_review_count = count_first_book_reviews(books_with_reviews)
print(first_book_review_count)

av_book_price = avarage_book_price(books_with_reviews)
print(av_book_price)


ratings = best_worst_rating_book(books_with_reviews)
print(ratings)
print_reviews_for_book(books_with_reviews)