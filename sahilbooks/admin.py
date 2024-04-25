from flask import Blueprint
from . import db
from .models import Categories, BookDetail
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():

    category1 = Categories( title='Sci-fi',image='SCI-FI.jpg', description = 'abc')
    category2 = Categories( title='fantasy',image='FANTASY.jpg', description = 'pqr')
   
    book1 = BookDetail(book_id=book1.id, image='t_cuddle.jpg', price=59.99,\
        date=datetime.datetime(2023, 5, 17),\
        name='Harry Potter',\
        description= 'World most popular and highest selling fantasy book') 
    book2 = BookDetail(book_id=book2.id, image='t_cuddle.jpg', price=100.50,\
        date=datetime.datetime(2023, 2, 1),\
        name='Rich Dad Poor Dad',\
        description= 'The book to change mindset about money learn how small financial decisions can help to create great wealth and how attitude towards money can provide make difference')
    book3 = BookDetail(book_id=book3.id, image='t_sand.jpg', price=180.50,\
        date=datetime.datetime(2023, 3, 10),\
        name='Think and Grow Rich',\
        description= 'want to know thoughts of Napoleon Hill on money this is the book of you are looking for')
    
    book1 = BookDetail(book_id=book1.id, image='t_cuddle.jpg', price=59.99,date=datetime.datetime(2023, 5, 17), name='Harry Potter', description= 'World most popular and highest selling fantasy book') 
    book2 = BookDetail(book_id=book2.id, image='t_cuddle.jpg', price=100.50, date=datetime.datetime(2023, 2, 1), name='Rich Dad Poor Dad', description= 'The book to change mindset about money learn how small financial decisions can help to create great wealth and how attitude towards money can provide make difference')
    book3 = BookDetail(book_id=book3.id, image='t_sand.jpg', price=180.50, date=datetime.datetime(2023, 3, 10), name='Think and Grow Rich', description= 'want to know thoughts of Napoleon Hill on money this is the book of you are looking for')

 
    try:
        db.session.add(category1)
        db.session.add(category2)
        db.session.commit()
        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.commit()
    except:
        return 'There was an issue adding the book'

