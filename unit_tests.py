import pytest
from classes import *

# basic tests for database 

def test_project_steps_table_exists(cursor):
    cursor.execute('select if from project_steps')
    rs = cursor.fetchall() #rs row set
    assert len(rs) == 0

## basically here I'm explicitly rolling back so the database can
## after each test wipe out the database and start with that fresh
## clean slate


# in our connection fixture we have on our fixture decorator (scope='module) that means that the connection fixture will stay,
# it won't get cleaned up at the end of each test so what this means is it will basically stay in stay in memory and it will maintain that connection with each test
# so a little bit more speed when we run our tests
@pytest.fixture(scope = 'module')
# reading password from the file to not hardcode it and to keep it secure (don't commit your password to youe repo)
def password():
    with open('pass.word') as f:
        pw = f.readline().strip()
        assert pw
# setting up the connection that Python test is going to use to make it to actually acces the database and it's gonna be closing the connection  after it yield
@pytest.fixture(scope = 'module')
def cnxn(password):
    cnxn = pyodbc.connect('DSN=bruisedthumb;UID=bruised;PWD={}'.format(password))
    yield cnxn.close()
# cursor which is going to be executing our sequel againts the database
# and at the end of that there's a rollback as well responsible for resetting our database 
# to that empty clean slate so we can populate it with more data for our next test
@pytest.fixture
def cursor(cnxn):
    cursor = cnxn.cursor()
    yield cursor
    cnxn.rollback()
    
### Now I want to reuse a single database connection
### instead of setting up a new database connection
### with every test

### here are fixtures that will set up our database before each test
### so the idea is that you have fixture that  is gonna set up or populate
### with each test ### example project in this case populate three different tables and put data into them 
### and then we can run our tests from there
 
@pytest.fixture
def checking_inserting_tables_data(cursor): # stmt - shortcut of staticmethod
    stmt = textwrap.dedent('''
    INSERT INTO projects(name, description)
    VALUES ('bookshelf', 'Building a bookshelf from birch playwood')
    ''')
    cursor.execute(stmt)
    stmt = 'SELECT @@IDENTITY'
    project_id = cursor.execute(stmt).fetchval()
    stmt = textwrap.dedent('''
    INSERT INTO project_supplies(project_id, name, quantity, unit_cost)
    VALUES ({project_id}, 'Bitch Playwood', 3, 48.50),
           ({project_id}, 'Wood Glue', 1, 5.99),
           ({project_id}, 'Screws', 2, 8.97)        
            ''')
    cursor.execute(stmt.format(project_id = project_id))
    yield project_id
    
## we are yielding project ID because usually  becauses when u run your test u're probably gonna use
## those IDs againsts in your tests to verify various things
 
 
# Simple test on database, keep it simple! :
# verify that I can connect at a database, make sure that pytest is running how I want
# it to e running

# test that checks if table exists
def test_table_exists(cursor):
    rs = cursor.execute('select id from some_table').fetchval()
    assert len(rs) == 0
    
def test_dupa():
    book = Book( )
    book.add_review(Review(rating=6))
    
    assert(book.average_rating() == 5.5)
    assert(isinstance(book.average_rating(), float))
    
def test_count_books():
    books = [Book(), Book()]
    
    count = count_books(books)
    
    assert(count == 2)