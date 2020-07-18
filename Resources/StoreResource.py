from typing import Optional
from Models.StoreModel import StoreModel
from flask_restful import Resource


class StoreResource(Resource):
    def get(self, name):
        store: Optional[StoreModel] = StoreModel.find_store_by_name(name)
        if store:
            return store.json_representation()

        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {"message": "The store already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An internal error occured"}, 500
        return store.json_representation(), 201

    def delete(self, name):
        store: Optional[StoreModel] = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store was successfully deleted"}
