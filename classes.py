import psycopg2



class Book:
 
    def __init__(self, rank, title, price, rating, author, year_of_publication, genre, url, review) -> None:
        self.rank = rank
        self.title = title
        self.price = price
        self.rating = rating
        self.author = author
        self.year_of_publication = year_of_publication
        self.genre = genre
        self.url = url
        self.review = list[Review]
    
    
class Review:
    
    def __init__ (self, sno, name, title, reviewer, rating, description, js_verified, date, timestamp, asin):
        self.sno = sno
        self.name = name
        self.title = title
        self.reviewer = reviewer
        self.rating = rating
        self.description = description
        self.js_verified = js_verified 
        self.date = date 
        self.timestamp = timestamp 
        self.asin = asin

