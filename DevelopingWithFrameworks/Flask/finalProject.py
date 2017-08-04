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
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[r.serialize for r in restaurants])

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
        return redirect(url_for('restaurants'))
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
        return redirect(url_for('restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=a_restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
    a_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(a_restaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=a_restaurant)


# @app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    r = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menuV2.html', restaurant=r, menu=menu)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[m.serialize for m in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def restaurant_menu_item_json(restaurant_id,menu_item_id):
    menu_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_item_id).one()

    return jsonify(MenuItem=[menu_item.serialize])

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def menu_item_new(restaurant_id):
    if request.method == 'POST':
        item = MenuItem()
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        item.restaurant_id = restaurant_id
        session.add(item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItemV2.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit', methods=['GET', 'POST'])
def menu_item_edit(restaurant_id, menu_item_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_item_id).one()
    if request.method == "POST":
        item.name = request.form['name']
        item.course = request.form['course']
        item.price = request.form['price']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItemV2.html', restaurant_id=restaurant_id,
                               menu_item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete', methods=['GET','POST'])
def menu_item_delete(restaurant_id, menu_item_id):
    menu_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_item_id).one()
    if request.method == "POST":
        session.delete(menu_item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItemV2.html', restaurant_id=restaurant_id, menu_item=menu_item)


if __name__ == '__main__':
    app.secret_key = '4b$3H7of7E!-KyU#QCTw#c7Bdj_4#5'
    app.debug = True
    app.run('0.0.0.0', port=8080)
