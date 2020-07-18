import sqlite3
from Models.UserModel import UserModel
from flask_restful import Resource, reqparse


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="The username field is required")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="The password field is required")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"success": False, "message": "That Username already exists, please try another"}, 400
        connection = sqlite3.connect("./Models/data.db")

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User has been created successfully."}, 201
