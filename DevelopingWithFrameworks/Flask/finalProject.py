from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/restaurants')
def restaurants():
    return "restaurant list"


@app.route('/restaurant/new')
def new_restaurant():
    return "Create new restaurant"


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
