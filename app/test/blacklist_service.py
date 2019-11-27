from app.main import db
from app.main.model.blacklist import BlacklistToken
from app.main.util.dry_util import *


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = create_response('success', 'Successfully logged out.')

        return response_object, 200
    except Exception as e:
        response_object = create_response('fail', e)

        return response_object, 200
