from datetime import datetime
import pytest
from classes import *


def test_avarage_rating():
    book = make_book_with_review( reviews = [
        make_review(rating=4),
        make_review(rating=5)
    ])
    assert book.average_rating() == 4.5
    assert isinstance(book.average_rating(), float)
    
def test_review_count() -> int:
    reviews = [
        make_review(),
        make_review(),
        make_review()
    ]
    assert(len(reviews) == 3)

def test_count_books():
    books = [make_book()]
    count = count_books(books)
    assert(count == 1)
    # check negative cases, for example a non-list argument
    with pytest.raises(TypeError):
        count_books('Invalid argument')
     
def test_add_review():
    #arrange
    book = make_book()
    initial_reviews_count = len(book.reviews)
    new_review = make_review()
    #act
    book.add_review(new_review)
    updated_reviews_count = len(book.reviews)
    assert updated_reviews_count == initial_reviews_count + 1
    assert new_review in book.reviews

def test_get_author():
    author='Rebecca Yarros'
    book = make_book(author = author)
    result = book.get_author()
    assert result == author
    
def test_count_first_book_reviews():
    book1 = make_book_with_review(reviews = [
        make_review(),
        make_review()
    ]) 
    book2 = make_book_with_review(reviews = [
        make_review()
        ])
    books = [book1, book2]
    result = count_first_book_reviews(books)
    assert result == 2

def test_avarage_book_price():
    book1 = make_book(price =2.0)
    book2 = make_book(price =2.0)
    books = [book1, book2]
    result = avarage_book_price(books)
    assert result == 2.0

def test_avarage_book_price_empty_list():
    empty_list = []
    result = avarage_book_price(empty_list)
    assert result == 0.0

def test_best_worst_rating_book():
    book1 = make_book_with_review(author = "Author1", reviews = [
        make_review(rating = 5),
        make_review(rating = 4)
    ])
    book2 = make_book_with_review(author = "Author2", reviews = [
        make_review(rating = 2),
        make_review(rating = 3)
        ])
    books = [book1, book2]
    result = best_worst_rating_book(books)
    expected_result = ((5, "Author1"), (2, "Author2"))
    assert result == expected_result

def test_book_with_most_reviews() -> tuple:
    book1 = make_book_with_review(author = "Author1", reviews = [
        make_review(),
        make_review()
    ])
    book2 = make_book_with_review(author = "Author2", reviews = [
        make_review(),
    ])
    books = [book1, book2]
    result = book_with_most_reviews(books)
    assert result == ('Author1', 2)

def test_year_of_publication_defference() -> int:
    book1 = make_book(year_of_publication=2022)
    book2 = make_book(year_of_publication=2020)
    books = [book1, book2]
    result = year_of_publication_defference(books)
    assert result == 2

def test_book_with_no_review() -> str:
    # case: Book with no reviews
    title = "Flame (The Empyrean, 2)"
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2022,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2 = Book(rank =3, title=title,price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating = 5)
    book1.add_review(review1)
    books = [book1, book2]
    result = book_with_no_review(books)
    assert result == title
    # case: All Books have reviews
    review2 = make_review(rating =2)
    book2.add_review(review2)
    books = [book1, book2]
    result = book_with_no_review(books)
    assert result is None

def test_most_fertile_reviewer() -> str:
    
    bo = make_book_with_review(reviews = [
        make_review(reviewer = 'Martyna'),
        make_review(reviewer = 'Martyna')
    ])
    bo2 = make_book_with_review(reviews = [
        make_review(reviewer = 'Martyna'),
        make_review(reviewer = 'Radek')
    ])
    books = [bo, bo2]
    result = most_fertile_reviewer(books)
    assert result == 'Martyna'

def test_get_most_fertile_authors() -> tuple:
    books_with_same_author =[
        make_book(title="Book1",author='Author2'),
        make_book(title="Book2",author='Author2'),
        make_book(title="Book3",author='Author2'),
        make_book(title="Book4",author='Author2')
    ]
    result = get_most_fertile_authors(books_with_same_author)
    assert result == ({'Author2': 4})

    less_than_five_books = [
        make_book(title="Book1",author='Author2'),
        make_book(title="Book2",author='Author3'),
        make_book(title="Book3",author='Author3')
    ]
    result = get_most_fertile_authors(less_than_five_books)
    assert result == ({'Author3': 2,'Author2': 1})
    
    more_than_five_authors = [
        make_book(title="Book1",author='Author1'),
        make_book(title="Book1",author='Author1'),
        make_book(title="Book1",author='Author1'),
        make_book(title="Book2",author='Author2'),
        make_book(title="Book2",author='Author2'),
        make_book(title="Book2",author='Author2'),
        make_book(title="Book2",author='Author2'),
        make_book(title="Book3",author='Author3'),
        make_book(title="Book4",author='Author4'),
        make_book(title="Book4",author='Author4'),
        make_book(title="Book4",author='Author4'),
        make_book(title="Book5",author='Author5'),
        make_book(title="Book5",author='Author5'),
        make_book(title="Book6",author='Author6'),
        make_book(title="Book6",author='Author6')
    ]
    result = get_most_fertile_authors(more_than_five_authors)
    assert result == ({'Author2': 4,'Author1': 3, 'Author4': 3,'Author5': 2, 'Author6': 2})

def make_review(sno=919.0, name='', reviewer='', rating=5, description='', js_verified='', timestamp='', asin=545261244) -> Review:
    return Review(sno, name, reviewer, rating, description, js_verified, datetime.now(), timestamp, asin)

def make_book(rank = 4.0, title = '', price = 34.0, rating = 3.4, author = '', year_of_publication = '', genre = '', url = '') -> Book:
    return Book(rank, title, price, rating, author, year_of_publication, genre, url)

def make_book_with_review(rank = 4.0, title = '', price = 34.0, rating = 3.4, author = '', year_of_publication = '', genre = '', url = '', reviews = []) -> Book:
    book = Book(rank, title, price, rating, author, year_of_publication, genre, url)
    for review in reviews:
        book.add_review(review)
    return book