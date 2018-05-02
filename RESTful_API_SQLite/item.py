import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        #items = result.fetchall()
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

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        try:
            self.insert(item)
        except Exception as error:
            print(error)
            return {'message': 'An error occurred inserting the item'}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        item = self.find_by_name(name)
        update_item = {'name': name, 'price': request_data['price']}

        if item:
            try:
                self.update(update_item)
            except Exception as error:
                print(error)
                return {'message': 'An error occurred updating the item'}, 500
        else:
            try:
                self.insert(update_item)
            except Exception as error:
                print(error)
                return {'message': 'An error occurred inserting the item'}, 500

        return item
