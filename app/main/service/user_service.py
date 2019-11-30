import uuid
import os
import datetime
from flask import request

from app.main import db
from app.main.model.user import User

from app.main.util.dry_util import create_response, thumbnail_resize, thumbnail_loc
from app.main.util.validate import Validate
from ..util.decorator import token_required
from app.main.service.auth_helper import Auth

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


@token_required
def save_thumbnail(args):

    user_id = Auth.get_logged_in_user(request)[0]['data']['user_id']
    check_user = User.query.filter_by(id=user_id).first()
    if not check_user:
        response_object = create_response('fail', 'please login first')
        return response_object

    img = args['thumbnail']
    img_type = img.mimetype

    img_name = ''

    if img_type == 'image/jpeg':
        img_name = thumbnail_resize(img)

    if img_name:
        old_image = check_user.thumbnail
        check_user.thumbnail = img_name
        db.session.commit()
        if old_image:
            full_old_path = f"{thumbnail_loc}\\{old_image}"
            if os.path.isfile(full_old_path):
                os.remove(full_old_path)
        response_object = create_response('success', 'your thumbnail updated')
        return response_object

    response_object = create_response('fail', 'please make shoure ur image type is jpg/jpeg')
    return response_object
