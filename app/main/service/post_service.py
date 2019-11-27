from flask import request
from app.main import db
from app.main.model.post import Post
from app.main.model.category import Category
from app.main.model.like import Like
from app.main.service.auth_helper import Auth
from app.main.util.dry_util import create_response
from app.main.util.validate import Validate
from ..util.decorator import token_required, admin_token_required

valid = Validate()


@token_required
def create_post(data):
    # check if author token exists
    user = Auth.get_logged_in_user(request)
    if (not valid.validate_length(data['title'], 10) or
            not valid.validate_length(data['body'], 30)):
        response_object = create_response('fail', 'The Minimum Length For Title 10 And body 30')
        return response_object

    post = Post.query.filter_by(title=data['title']).first()
    if not post:
        new_post = Post(
            title=data['title'],
            body=data['body'],
            author=user[0]['data']['user_id'])

        db.session.add(new_post)
        db.session.commit()

        if data['category']:
            for cat in data['category']:
                n_cat = add_category(cat)
                n_cat.categories.append(new_post)

            db.session.commit()
        response_object = create_response('success', 'your post created.')
        return response_object, 200
    else:
        response_object = create_response(
            'fail', 'post already exists. Please Choose Unique Title.')

    return response_object, 400


def get_all_posts():
    return Post.query.all()


@token_required
def add_category(cat):
    if not valid.validate_length(cat, 2):
        response_object = create_response('fail', 'Category Minimum Length 2.')
        return response_object
    check_cat = Category.query.filter_by(cat=cat).first()
    if check_cat:
        return check_cat
    else:
        new_cat = Category(cat=cat)
        db.session.add(new_cat)
        db.session.commit()
        return new_cat


def get_a_post(post_id):
    return Post.query.filter_by(id=post_id).first()


@token_required
def add_remove_like(post_id):
    post = get_a_post(post_id)
    user_id = Auth.get_logged_in_user(request)[0]['data']['user_id']

    if post.author == user_id:
        response_object = create_response(
            'fail', 'You Cant Like Your Own Post')
        return response_object

    like = Like.query.filter_by(post_id=post.id, user_id=user_id).first()

    if not like:
        like = Like(post_id=post.id, user_id=user_id)
        db.session.add(like)
    else:
        db.session.delete(like)
    db.session.commit()

    if not like:
        response_object = create_response(
            'fail', 'Somthing Whent Rong When we Trying To Add Your Support For This Post')
    else:
        response_object = create_response('success', 'Every Thing Done')

    return response_object


@admin_token_required
def remove_post(post_id):
    post = get_a_post(post_id)

    if not post:
        response_object = create_response('fail', 'This Post Not Exist')
        return response_object

    db.session.delete(post)
    db.session.commit()

    response_object = create_response('Success', 'post deleted')
    return response_object
