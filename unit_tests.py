import pytest
from classes import *
from datetime import datetime


# basic tests for database 

#def test_project_steps_table_exists(cursor):
#    cursor.execute('select if from project_steps')
#    rs = cursor.fetchall() #rs row set
#    assert len(rs) == 0
#
### basically here I'm explicitly rolling back so the database can
### after each test wipe out the database and start with that fresh
### clean slate
#
#
## in our connection fixture we have on our fixture decorator (scope='module) that means that the connection fixture will stay,
## it won't get cleaned up at the end of each test so what this means is it will basically stay in stay in memory and it will maintain that connection with each test
## so a little bit more speed when we run our tests
#@pytest.fixture(scope = 'module')
## reading password from the file to not hardcode it and to keep it secure (don't commit your password to youe repo)
#def password():
#    with open('pass.word') as f:
#        pw = f.readline().strip()
#        assert pw
## setting up the connection that Python test is going to use to make it to actually acces the database and it's gonna be closing the connection  after it yield
#@pytest.fixture(scope = 'module')
#def cnxn(password):
#    cnxn = pyodbc.connect('DSN=bruisedthumb;UID=bruised;PWD={}'.format(password))
#    yield cnxn.close()
## cursor which is going to be executing our sequel againts the database
## and at the end of that there's a rollback as well responsible for resetting our database 
## to that empty clean slate so we can populate it with more data for our next test
#@pytest.fixture
#def cursor(cnxn):
#    cursor = cnxn.cursor()
#    yield cursor
#    cnxn.rollback()
#    
#### Now I want to reuse a single database connection
#### instead of setting up a new database connection
#### with every test
#
#### here are fixtures that will set up our database before each test
#### so the idea is that you have fixture that  is gonna set up or populate
#### with each test ### example project in this case populate three different tables and put data into them 
#### and then we can run our tests from there
# 
#@pytest.fixture
#def checking_inserting_tables_data(cursor): # stmt - shortcut of staticmethod
#    stmt = textwrap.dedent('''
#    INSERT INTO projects(name, description)
#    VALUES ('bookshelf', 'Building a bookshelf from birch playwood')
#    ''')
#    cursor.execute(stmt)
#    stmt = 'SELECT @@IDENTITY'
#    project_id = cursor.execute(stmt).fetchval()
#    stmt = textwrap.dedent('''
#    INSERT INTO project_supplies(project_id, name, quantity, unit_cost)
#    VALUES ({project_id}, 'Bitch Playwood', 3, 48.50),
#           ({project_id}, 'Wood Glue', 1, 5.99),
#           ({project_id}, 'Screws', 2, 8.97)        
#            ''')
#    cursor.execute(stmt.format(project_id = project_id))
#    yield project_id
#    
### we are yielding project ID because usually  becauses when u run your test u're probably gonna use
### those IDs againsts in your tests to verify various things
# 
# 
## Simple test on database, keep it simple! :
## verify that I can connect at a database, make sure that pytest is running how I want
## it to e running
#
## test that checks if table exists
#def test_table_exists(cursor):
#    rs = cursor.execute('select id from some_table').fetchval()
#    assert len(rs) == 0
#    
def test_avarage_rating():
    book = Book( rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
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
    # arrange
    author='Rebecca Yarros'
    book_instance = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    #act
    result = book_instance.get_author()
    assert result == author
    

def test_count_first_book_reviews():
    #arrange
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =18.42,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book1.add_review('Review1')
    book1.add_review('Review2')

    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =18.46,rating =4.0,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2.add_review("Review3")

    books = [book1, book2]

    #act
    result = count_first_book_reviews(books)
    assert result == 2

def test_avarage_book_price():
    #arrange
    book1 = Book(rank =1, title="Iron Flame (The Empyrean, 2)",price =2.0,rating =4.1,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book1.add_review('Review1')
    book1.add_review('Review2')

    book2 = Book(rank =3, title=" Flame (The Empyrean, 2)",price =2.0,rating =4.0,author='Rebecca Yarros',year_of_publication=2023,genre='Fantasy Romance',url ='amazon.com/Iron-Flame-Empyrean-Rebecca-Yarros/dp/1649374178/ref=zg_bs_g_books_sccl_1/143-9831347-1043253?psc=1')
    book2.add_review("Review3")

    books = [book1, book2]
    #act
    result = avarage_book_price(books)
    assert result == 2.0

def test_avarage_book_price_empty_list():
    empty_list = []
    result = avarage_book_price(empty_list)
    assert result == 0.0

def test_print_reviews_for_book():

    pass

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

def test_book_with_most_reviews(books_with_reviews: list[Book]) -> tuple:
    pass

def test_year_of_publication_defference(books_with_reviews: list[Book]) -> int:
    pass

def test_book_with_no_review(books_with_reviews: list[Book]) -> str:
    pass

def test_most_fertile_reviewer(books_with_reviews: List[Book]) -> str:
    pass

def test_get_most_fertile_authors(books_with_reviews: list[Book]) -> tuple:
    pass

def make_review(sno=919.0, name='', reviewer='', rating=5, description='', js_verified='', timestamp='', asin=545261244) -> Review:
    return Review(sno, name, reviewer, rating, description, js_verified, datetime.now(), timestamp, asin)

def make_book(rank = 4.0, title = '', price = 34.0, rating = 3.4, author = '', year_of_publication = int, genre = '', url = '') -> Book:
    return Book(rank, title, price, rating, author, year_of_publication, genre, url)