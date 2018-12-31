from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': "Store '{}' not found".format(name)}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_in_DB()
        except:
            return {"message", "An error occured while inserting a store in DB"}, 500

        return store.json(), 201

    def delete(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_DB()
                return {'message': "A store with name '{}' is deleted".format(name)}, 201
            except:
                return {"message", "An error occrued while deleting a store in DB"}, 500
        else:
            return {'message': "store '{}' is does not exist".format(name)}, 201


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
