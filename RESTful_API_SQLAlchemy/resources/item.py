import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from RESTful_API_SQLAlchemy.models.item import ItemModel


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        # items = result.fetchall()
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert()
        except Exception as error:
            print(error)
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel(name, request_data['price'])

        if item:
            try:
                update_item.update()
            except Exception as error:
                print(error)
                return {'message': 'An error occurred updating the item'}, 500
        else:
            try:
                update_item.insert()
            except Exception as error:
                print(error)
                return {'message': 'An error occurred inserting the item'}, 500

        return update_item.json()
