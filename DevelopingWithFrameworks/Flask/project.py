from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:MenuID>/JSON')
def menuItemJSON(restaurant_id, MenuID):
    item = session.query(MenuItem).filter_by(id=MenuID).one()
    return jsonify(MenuItem=item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return(render_template('menu.html', restaurant = restaurant, items = items))

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == "POST":
        old_name = editedItem.name
        if request.form['name']:
            editedItem.name = request.form["name"]

        session.add(editedItem)
        session.commit()
        flash("{} changed to {}".format(old_name,editedItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id,
                        MenuID=MenuID, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/', methods=["GET","POST"])
def deleteMenuItem(restaurant_id, MenuID):
    menu_item = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == "POST":
        session.delete(menu_item)
        session.commit()
        flash('{} deleted'.format(menu_item.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, i=menu_item)

if __name__ == '__main__':
    app.secret_key='Secret Key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
