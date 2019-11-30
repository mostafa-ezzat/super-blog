from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, save_thumbnail
from app.main.util.file_parse import jpeg_upload

api = UserDto.api
_user = UserDto.user
_userpost = UserDto.many_user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        print(data)
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.expect(_userpost, validate=True)
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_userpost)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        return user


@api.route('/thumbnail/upload')
class my_file_upload(Resource):
    @api.expect(jpeg_upload)
    def post(self):
        args = jpeg_upload.parse_args()
        res = save_thumbnail(args)
        return res
