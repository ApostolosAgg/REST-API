from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field is mandatory")

    parser.add_argument('password',
    type=str,
    required=True,
    help="This field is mandatory")

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "User '{}' already exists".format(data['username'])}, 400

        user = UserModel(data['username'], data['password'])
        try:
            user.save_in_DB()
        except:
            return {"message", "An error occured while inserting a user in DB"}, 500

        return {'message': "User'{}' is succesfully created".format(data['username'])}, 201
