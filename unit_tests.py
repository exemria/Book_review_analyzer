import pytest
from classes import *
from datetime import datetime


def test_avarage_rating():
    book = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating=5)
    review2 = make_review(rating=4)
    
    book.add_review(review1)
    book.add_review(review2)
    
    assert book.average_rating() == 4.5
    assert isinstance(book.average_rating(), float)
    
def test_review_count() -> int:
    reviews = [
        make_review(),
        make_review(rating=1),
        make_review(description="w miarę dobra")
    ]
    assert(len(reviews) == 3)

def test_count_books():
    books = [Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')] 
    count = count_books(books)
    assert(count == 1)
     
def test_load_books() -> List[Book]:
    pass

def test_add_review():
    #arrange
    book = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1') 
    initial_reviews_count = len(book.reviews)
    new_review = " La la la"
    #act
    book.add_review(new_review)
    updated_reviews_count = len(book.reviews)
    assert updated_reviews_count == initial_reviews_count + 1
    assert new_review in book.reviews

def test_get_author():
    author='Rebecca Yarros'
    book_instance = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    result = book_instance.get_author()
    assert result == author
    
def test_count_first_book_reviews():
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book1.add_review('Review1')
    book1.add_review('Review2')
    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =18.46,rating =4.0,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2.add_review("Review3")
    books = [book1, book2]
    
    result = count_first_book_reviews(books)
    assert result == 2

def test_avarage_book_price():
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book1.add_review('Review1')
    book1.add_review('Review2')
    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2.add_review("Review3")
    books = [book1, book2]

    result = avarage_book_price(books)
    assert result == 2.0

def test_avarage_book_price_empty_list():
    empty_list = []
    result = avarage_book_price(empty_list)
    assert result == 0.0

def test_best_worst_rating_book():
    
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating = 5)
    book1.add_review(review1)
    review2 = make_review(rating = 4)
    book1.add_review(review2)

    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review3 = make_review( rating = 2)
    book2.add_review(review3)
    review4 = make_review(rating = 3)
    book2.add_review(review4)

    books = [book1, book2]
    result = best_worst_rating_book(books)
    expected_result = ((5, "Author1"), (2, "Author2"))
    assert result == expected_result

def test_book_with_most_reviews() -> tuple:
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating = 5)
    book1.add_review(review1)
    review2 = make_review(rating = 4)
    book1.add_review(review2)

    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review3 = make_review( rating = 2)
    book2.add_review(review3)
    books = [book1, book2]

    result = book_with_most_reviews(books)
    assert result == ('Author1', 2)

def test_year_of_publication_defference() -> int:
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2022,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    books = [book1, book2]
    result = year_of_publication_defference(books)
    assert result == 2

def test_book_with_no_review() -> str:
    # case: Book with no reviews
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2022,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2 = Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating = 5)
    book1.add_review(review1)
    books = [book1, book2]
    result = book_with_no_review(books)
    assert result == "Flame (The Empyrean, 2)"
    # case: All Books have reviews
    review2 = make_review(rating =2)
    book2.add_review(review2)
    books = [book1, book2]
    result = book_with_no_review(books)
    assert result is None

def test_most_fertile_reviewer() -> str:
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author1',year_of_publication=2022,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2 = Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    review1 = make_review(rating = 5, reviewer = 'Martyna')
    review2 = make_review(rating =2, reviewer = 'Martyna')
    review3 = make_review(rating =2, reviewer = 'Martyna')
    review4 = make_review(rating =2, reviewer = 'Martyna')
    review5 = make_review(rating =2, reviewer = 'Radek')
    book1.add_review(review1)
    book1.add_review(review2)
    book1.add_review(review3)
    book1.add_review(review4)
    book2.add_review(review5)
    books = [book1, book2]
    result = most_fertile_reviewer(books)
    assert result == 'Martyna'

def test_get_most_fertile_authors() -> tuple:
    books_with_same_author =[
        Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =1.0,author='Author2',year_of_publication=2022,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1'),
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1'),
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1'),
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    ]
    result = get_most_fertile_authors(books_with_same_author)
    assert result == ({'Author2': 4})

    less_than_five_books = [
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author3',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1'),
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author3',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1'),
        Book(rank =3, title="Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Author2',year_of_publication=2020,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    ]
    result = get_most_fertile_authors(less_than_five_books)
    assert result == ({'Author3': 2,'Author2': 1})

def make_review(sno=919.0, name='', reviewer='', rating=5, description='', js_verified='', timestamp='', asin=545261244) -> Review:
    return Review(sno, name, reviewer, rating, description, js_verified, datetime.now(), timestamp, asin)

def make_book(rank = 4.0, title = '', price = 34.0, rating = 3.4, author = '', year_of_publication = int, genre = '', url = '') -> Book:
    return Book(rank, title, price, rating, author, year_of_publication, genre, url)