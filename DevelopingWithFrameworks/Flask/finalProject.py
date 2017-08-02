from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
               {'name':'Blue Burgers', 'id':'2'},
               {'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'},
          {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
          {'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
          {'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
          {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/restaurants')
@app.route('/')
def list_restaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new',methods=['GET','POST'])
def new_restaurant():
    if request.method == 'POST':

        return redirect(url_for('list_restaurants'))
    else:
        return render_template('newRestaurant.html')


# Saved for future restaurant info page
# @app.route('/restaurants/<int:restaurant_id>')
# def restaurant_menu(restaurant_id):
#     return "Menu for restaurant {}".format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/edit')
def restaurant_edit(restaurant_id):
    return "Edited restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete')
def restaurant_delete(restaurant_id):
    return "Deleted restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    return "Display menu for restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def menu_item_new(restaurant_id):
    return "Created menu item for restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit')
def menu_item_edit(restaurant_id, menu_item_id):
    return "Edited menu item {} for restaurant {}".format(menu_item_id, restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete')
def menu_item_delete(restaurant_id, menu_item_id):
    return "Deleted menu item {} for restaurant {}".format(menu_item_id, restaurant_id)


if __name__ == '__main__':
    app.secret_key = '4b$3H7of7E!-KyU#QCTw#c7Bdj_4#5'
    app.debug = True
    app.run('0.0.0.0', port=8080)



