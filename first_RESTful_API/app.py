from flask import Flask, request

from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from first_RESTful_API.security import authentication_user, identity

app = Flask(__name__)
app.secret_key = 'teste'
api = Api(app)

jwt = JWT(app, authentication_user, identity)  # /auth

items = []


class Items(Resource):
    def get(self):
        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists'}, 400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = next(filter(lambda i: i['name'] != name, items), None)
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda i: i['name'] == name, items), None)
        if item:
            item.update(request_data)
        else:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)

        return item


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
