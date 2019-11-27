from flask import request
from app.main import db
from app.main.model.comment import Comment
from app.main.model.post import Post
from app.main.service.auth_helper import Auth
from app.main.util.dry_util import create_response
from app.main.util.validate import Validate
from ..util.decorator import token_required

valid = Validate()


@token_required
def create_comment(data, post_id):
    # check if author token exists
    user = Auth.get_logged_in_user(request)
    if user[1] != 200:
        response_object = create_response('fail', 'Auth Token Required.')
        return response_object
    else:
        if (not valid.validate_exist(post_id) or
                not valid.validate_length(data.get('body'), 5)):
            response_object = create_response(
                'fail', 'please make sure everything exist')
            return response_object

        # check if post exsit
        check_post = Post.query.filter_by(id=post_id).first()
        if not check_post:
            response_object = create_response('fail', 'This Post Not Exist')
            return response_object

        parent = 0
        user = user[0]['data']['user_id']

        if (valid.validate_exist(data.get('parent_id')) and
                data.get('parent_id') > 0):
            # check if parent have parent
            parent = data.get('parent_id')
            pComment = Comment.query.filter_by(id=parent).first()
            if pComment.parent_id > 0:
                response_object = create_response('fail', 'sorry we cant now')
                return response_object

        comment = Comment(post_id=post_id,
                          user_id=user,
                          body=data.get('body'),
                          parent_id=parent)
        db.session.add(comment)
        db.session.commit()

        response_object = create_response('success',
                                          'your comment added successfully')
        return response_object


def get_a_comment(comment_id):
    return Comment.query.filter_by(id=comment_id).first()


@token_required
def delete_a_comment(comment_id):
    user = Auth.get_logged_in_user(request)

    check_comment = Comment.query.filter_by(
        id=comment_id, user_id=user[0]['data']['user_id']).first()

    if not check_comment:
        response_object = create_response('fail', 'this comment not exist')
        return response_object

    db.session.delete(check_comment)
    db.session.commit()

    response_object = create_response('success', 'comment deleted')
    return response_object


def get_post_comment(post_id):
    check_post = Post.query.filter_by(id=post_id).first()

    if not check_post:
        response_object = create_response('fail', 'this post not exist')
        return response_object

    comment = Comment.query.filter_by(post_id=check_post.id, parent_id=0).all()

    return comment
