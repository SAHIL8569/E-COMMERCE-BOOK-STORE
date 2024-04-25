from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Order, BookDetail, Categories
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

# Home page
@main_bp.route('/')
def index():
    books = db.session.scalars(db.select(Categories)).all()
    return render_template('index.html', books=books)

# View all the books
@main_bp.route('/bookdetail/<int:book_id>')
def bookdetail(book_id):
   books = db.session.scalars(db.select(BookDetail).where(BookDetail.book_id==book_id)).all()
   return render_template('bookdetails.html', books=books)

# Referred to as "Basket" to the user
@main_bp.route('/order/', methods=['POST', 'GET'])
def order():
    book_id = request.values.get('book_id')
    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id/session is stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status=False, first_name='', surname='', email='', phone='', total_cost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Failed at creating a new order!')
            order = None
    
    # calculate total price
    total_price = 0
    if order is not None:
        for book in order.item_detail:
            total_price += book.price
    
    # are we adding an item?
    if book_id is not None and order is not None:
       book = db.session.scalar(db.select(BookDetail).where(BookDetail.id==book_id))
       if book not in order.item_detail:
           try:
               order.item_detail.append(book)
               db.session.commit()
           except:
               flash('There was an issue adding the item to your basket',category='danger')
           return redirect(url_for('main.order'))
       else:
           flash('There is already one of these in the basket')
           return redirect(url_for('main.order'))
    print(f'Values: {order}')
    return render_template('order.html', order=order.item_detail, total_price=total_price)

# Delete specific basket items
# Note this route cannot accept GET requests now
@main_bp.route('/deleteorderitem/', methods=['POST', 'GET'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        item_to_delete = db.session.scalar(db.select(BookDetail).where(BookDetail.id==id))
        try:
            order.item_detail.remove(item_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder/')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

# Complete the order
@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.first_name = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            total_cost = 0
            for book in order.item_detail:
                total_cost += book.price
            order.total_cost = total_cost   
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

@main_bp.route('/books')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search) # substrings will match
    books = BookDetail.query.filter(BookDetail.description.like(search)).all()
    return render_template('search.html', books=books)
