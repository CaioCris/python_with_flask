from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from RESTful_API_SQLite.item import Items, Item
from RESTful_API_SQLite.user import UserRegister
from RESTful_API_SQLite.security import authentication_user, identity

app = Flask(__name__)
app.secret_key = 'teste'
api = Api(app)

jwt = JWT(app, authentication_user, identity)  # /auth

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
