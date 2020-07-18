from Models.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json_representation(self):
        return {'name': self.name, "items": [item.json_representation() for item in self.items.all()]}

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_store_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()