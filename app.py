from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity

from Models.db import db
from Resources.UserRegisterResource import UserRegister
from Resources.ItemResource import Item, ItemList
from Resources.StoreResource import StoreResource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Models/data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "dflkqjdf9wh4iew0e2349203-q[da;kdfjfhjuas84u5238090joidfa;s"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# create an auth endpoint with
jwt = JWT(app, authentication, identity)

# add resource and resource endpoints
api.add_resource(Item, "/item/<string:name>/")
api.add_resource(ItemList, "/items/")
api.add_resource(UserRegister, "/register/")
api.add_resource(StoreResource, "/store/<string:name>")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
