from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
               {'name': 'Blue Burgers', 'id': '2'},
               {'name': 'Taco Hut', 'id': '3'}]

# Fake Menu Items
items = [
    {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
    {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
     'id': '2'},
    {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
     'id': '3'},
    {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
    {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
     'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}
items_empty = []

@app.route('/restaurants')
@app.route('/')
def list_restaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':

        return redirect(url_for('list_restaurants'))
    else:
        return render_template('newRestaurant.html')


# Saved for future restaurant info page
# @app.route('/restaurants/<int:restaurant_id>')
# def restaurant_menu(restaurant_id):
#     return "Menu for restaurant {}".format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def restaurant_edit(restaurant_id):
    a_restaurant = restaurants[restaurant_id - 1]
    if request.method == "POST":
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=a_restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
    a_restaurant = restaurants[restaurant_id - 1]
    if request.method == "POST":
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
