import sqlite3
from typing import Optional
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
from Models.ItemModel import ItemModel

items = []  # list to hold a collection of items


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=str,
                        required=True,
                        help="This field is required")
    parser.add_argument("storeId",
                        type=str,
                        required=True,
                        help="This field is required")

    @jwt_required()
    def get(self, name):
        item = None
        item_object: Optional[ItemModel] = ItemModel.find_by_name(name)
        if item_object:
            item = item_object.json_representation()

        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        Item.parser.add_argument('name',
                                 type=str,
                                 required=True,
                                 help="This Field is required"
                                 )
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(data['name']):
            return {'success': False, 'message': 'An item with that name already exists'}
        item = ItemModel(**data)
        item.save_to_db()

        return {"item": item.json_representation()}, 201

    @jwt_required()
    def delete(self, name):
        item: Optional[ItemModel] = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"success": True, "message": "Item deleted successfully"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item:
            item.update(request_data)
        else:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        return {"message": "Item updated successfully", "item": item}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect("./Models/data.db")
        cursor = connection.cursor()
        query = "Select * from items"
        result = cursor.execute(query)
        rows = result.fetchall()
        all_items = list(map(lambda x: {"id": x[0], "name": x[1], "price": x[2]}, rows))
        return {"items": all_items}

    @jwt_required()
    def post(self):
        new_items = []
        request_data = request.get_json()
        print(request_data)
        for data in request_data:
            item = {"name": data['name'], "price": data['price']}
            items.append(item)
            new_items.append(item)
        return new_items, 201
