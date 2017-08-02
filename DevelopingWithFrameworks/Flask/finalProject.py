from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants')
@app.route('/')
def list_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        r = Restaurant()
        r.name = request.form.get('name')
        if (r.name):
            session.add(r)
            session.commit()
        else:
            flash("No name given for Restaurant...not created")
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('newRestaurant.html')


# Saved for future restaurant info page
# @app.route('/restaurants/<int:restaurant_id>')
# def restaurant_menu(restaurant_id):
#     return "Menu for restaurant {}".format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def restaurant_edit(restaurant_id):
    a_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        a_restaurant.name = request.form['name']
        session.add(a_restaurant)
        session.commit()
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=a_restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
    a_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(a_restaurant)
        session.commit()
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=a_restaurant)


# @app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant_name = restaurants[restaurant_id - 1].get('name')
    menu = items_empty
    return render_template('menuV2.html', restaurant_name=restaurant_name,
                           menu=menu)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def menu_item_new(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form.get('price')
        description = request.form.get('description')
        course = request.form.get('course')
        out = '''
            name={}\n
            description={}\n
            price={}\n
            course={}
        '''.format(name, description, price, course)
        print(out)
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItemV2.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit', methods=['GET', 'POST'])
def menu_item_edit(restaurant_id, menu_item_id):
    menu_item = items[menu_item_id - 1]
    if request.method == "POST":
        name = request.form['name']
        price = request.form.get('price')
        description = request.form.get('description')
        course = request.form.get('course')
        out = '''
            name={}\n
            description={}\n
            price={}\n
            course={}
        '''.format(name, description, price, course)
        print(out)
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItemV2.html', restaurant_id=restaurant_id,
                               menu_item=menu_item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete', methods=['GET','POST'])
def menu_item_delete(restaurant_id, menu_item_id):
    menu_item = items[menu_item_id-1]
    if request.method == "POST":

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItemV2.html', restaurant_id=restaurant_id, menu_item=menu_item)


if __name__ == '__main__':
    app.secret_key = '4b$3H7of7E!-KyU#QCTw#c7Bdj_4#5'
    app.debug = True
    app.run('0.0.0.0', port=8080)
