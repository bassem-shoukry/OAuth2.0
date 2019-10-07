from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = 'IKOI24X21BJB0BUFQPRDSPBSKCKU2NT5UEKB4UQHPEV5AKH1'

foursquare_client_secret = 'TOIEFBMU1J03KLOK1GPJSONQYVTOMINIXNKBDBEADMS5WMW1'

google_api_key = 'AIzaSyA0NaULlDsrzIkZDlO7fy21inrkQaKF4Hk'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        restaurants  = session.query(Restaurant).all()
        return jsonify(resturants=[i.serialize for i in restaurants ])
    elif request.method == 'POST':
        location = request.args.get('location','')
        mealType = request.args.get('mealType','')
        restaurant_info = findARestaurant(location,mealType)
        if restaurant_info != "No Restaurants Found":
            restaurant = Restaurant(restaurant_name=unicode(restaurant_info['name']),
                                    restaurant_address=unicode(restaurant_info['address']),
                                    restaurant_image=restaurant_info['image'])
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant=restaurant.serialize)
        else:
            return jsonify({"error": "No Restaurants Found for %s in %s" % (mealType, location)})

# YOUR CODE HERE

@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'GET':
        # RETURN A SPECIFIC RESTAURANT
        return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'PUT':
        # UPDATE A SPECIFIC RESTAURANT
        address = request.args.get('address')
        image = request.args.get('image')
        name = request.args.get('name')
        if address:
            restaurant.restaurant_address = address
        if image:
            restaurant.restaurant_image = image
        if name:
            restaurant.restaurant_name = name
        session.commit()
        return jsonify(restaurant=restaurant.serialize)

    elif request.method == 'DELETE':
        session.delete(restaurant)
        session.commit()
        return "Restaurant Deleted"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)