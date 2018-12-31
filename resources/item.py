from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field is mandatory"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item must have store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item {} not found".format(name)}, 404

    def post(self, name):
        data = self.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        if item.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        try:
            item.save_in_DB()
        except:
            return {"message", "An error occured while inserting an element in DB"}, 500

        return item.json(), 201

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        try:
            item.save_in_DB()
        except:
            return {"message", "An error occrued while saving an item in DB"}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_DB()
                return {'message': "An item with name '{}' is deleted".format(name)}, 201
            except:
                return {"message", "An error occrued while deleting an item in DB"}, 500
        else:
            return {'message': "item '{}' is does not exist".format(name)}, 201

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(),ItemModel.query.all()))}
