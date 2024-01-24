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

    def get_author(self):
        return self.author
        
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
    if not isinstance(books_with_reviews, list):
        raise TypeError("Input must be a list of books.")
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

def book_with_most_reviews(books_with_reviews: list[Book]) -> tuple: # not sure if it's works correct
    count_authors_reviews = {}
    for book in books_with_reviews:
        for review in book.reviews:
            author = book.author
            if author in count_authors_reviews:
                count_authors_reviews[author] += 1
            else:
                count_authors_reviews[author] = 1

    max_amout_of_reviews ={key : val for key, val in sorted(count_authors_reviews.items(), key =lambda x: x[1], reverse = True )}
    first_element = next(iter(max_amout_of_reviews.items()))
    return first_element

def year_of_publication_defference(books_with_reviews: list[Book]) -> int:
    years = [book.year_of_publication for book in books_with_reviews]
    max_year = int(max(years))
    min_year = int(min(years))
    result = max_year - min_year
    return result

def book_with_no_review(books_with_reviews: list[Book]) -> str:
    for book in books_with_reviews:
        has_review = any(book.reviews)
        if not has_review:
            return book.title
    return None

def most_fertile_reviewer(books_with_reviews: List[Book]) -> str:
    count_reviewers = {}
    for book in books_with_reviews:
        for review in book.reviews:
            reviewer = review.reviewer
            if reviewer in count_reviewers:
                count_reviewers[reviewer] += 1
            else:
                count_reviewers[reviewer] = 1

    max_reviews = max(count_reviewers.items(), key=lambda x: x[1], default=None)
    if max_reviews:
        return max_reviews[0]
    else:
        return "No reviewers found."

def get_most_fertile_authors(books_with_reviews: list[Book]) -> tuple:
    count_author_books = {}
    for book in books_with_reviews:
        author = book.author
        if author in count_author_books:
            count_author_books[author] += 1
        else:
            count_author_books[author] = 1

    sorted_dict = {key : val for key, val in sorted(count_author_books.items(), key =lambda x: x[1], reverse = True )}
    res = dict(list(sorted_dict.items())[0: 5])
    return res


    

    #def get_books_of_author(self) -> dict:
    #    books_and_authors = {}
    #        books_and_authors[self.author] = self.title
    #    return books_with_reviews

books_with_reviews = load_books()

how_many = count_books(books_with_reviews)
print(how_many)

first_book_review_count = count_first_book_reviews(books_with_reviews)
print(first_book_review_count)

av_book_price = avarage_book_price(books_with_reviews)
print(av_book_price)

authors_books = get_most_fertile_authors(books_with_reviews)
print(authors_books)

ratings = best_worst_rating_book(books_with_reviews)
print(ratings)
#print_reviews_for_book(books_with_reviews)
defference = year_of_publication_defference(books_with_reviews)
print(defference)

max_reviews = book_with_most_reviews(books_with_reviews)
print(max_reviews)

no_review = book_with_no_review(books_with_reviews)
print(no_review)

rev = most_fertile_reviewer(books_with_reviews)
print(rev)