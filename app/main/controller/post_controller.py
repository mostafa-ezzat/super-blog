from flask import request
from flask_restplus import Resource

from ..util.dto import PostDto, LikeDto
from ..service.post_service import create_post, get_all_posts, get_a_post, add_remove_like, remove_post

api = PostDto.api
_post = PostDto.post


@api.route('/')
class PostList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_post, envelope='data')
    def get(self):
        """List all Created Posts"""
        return get_all_posts()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new post')
    @api.expect(_post, validate=True)
    def post(self):
        """Creates a new Post """
        data = request.json
        return create_post(data=data)


@api.route('/<int:post_id>')
@api.param('post_id', 'The Post Identifier')
@api.response(404, 'Post not found.')
class User(Resource):
    @api.doc('get a post')
    @api.marshal_with(_post)
    # @api.expect(_post_likes)
    def get(self, post_id):
        """get a post given its identifier"""
        post = get_a_post(post_id)
        if not post:
            api.abort(400, 'This Post Not Found', status='fail')
        else:
            return post


@api.route('/<int:post_id>/like')
@api.param('post_id', 'The Post Identifier')
@api.response(404, 'Post not found.')
class LikePost(Resource):
    @api.doc('Add or remove like')
    def get(self, post_id):
        """Add Or Remove Like"""
        post = add_remove_like(post_id)
        return post


@api.route('/<int:post_id>/del')
class RemovePost(Resource):
    @api.doc('Add or remove like')
    def get(self, post_id):
        """Remove Post"""
        post = remove_post(post_id)
        return post
