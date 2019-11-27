import uuid
import datetime

from app.main import db
from app.main.model.user import User

from app.main.util.dry_util import create_response
from app.main.util.validate import Validate

valid = Validate()


def save_new_user(data):
    # validate inputs
    if (
        not valid.validate_exist(data['email']) or
        not valid.validate_length(data['username'], 4) or
        not valid.validate_length(data['password'], 7)
    ):
        response_object = create_response('fail', 'Please Check Your Inputs Meet Our Needs')
        return response_object

    # check if email valid
    if not valid.validate_email(data['email']):
        response_object = create_response('fail', 'Please Enter Valid Email.')
        return response_object

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = create_response('fail', 'User already exists. Please Log in.')
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = create_response('success', 'Successfully registered.', {
            'Authorization': auth_token.decode()})
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
