from flask import request
from flask_restplus import Resource

from ..util.dto import CommentDto
from ..service.comment_service import create_comment, get_a_comment, delete_a_comment, get_post_comment


api = CommentDto.api
_comment = CommentDto.comment
_rescomment = CommentDto.rescomment


@api.route('/')
class Comment(Resource):
    def get(self):
        return 'Comments'


@api.route('/<int:comment_id>/get')
class GetAComment(Resource):
    @api.doc('Get A Spisific Comment')
    @api.marshal_list_with(_rescomment, envelope='data')
    def get(self, comment_id):
        """ Get Spisific Comment """
        comment = get_a_comment(comment_id)
        return comment


@api.route('/<int:post_id>/add')
class AddComment(Resource):
    @api.response(200, 'Comment Added.')
    @api.doc('Add New Comment To Post')
    @api.expect(_comment, validate=True)
    def post(self, post_id):
        """Creates a new Comment """
        data = request.json
        comment = create_comment(data=data, post_id=post_id)
        return comment


@api.route('/post/<int:post_id>')
class PostComments(Resource):
    @api.response(200, 'Comment Exist')
    @api.doc('Get Post Comments')
    @api.marshal_list_with(_rescomment, envelope='data')
    def get(self, post_id):
        """Get Post Comments"""
        comment = get_post_comment(post_id=post_id)
        return comment


@api.route('/<int:comment_id>/del')
class DeleteAComment(Resource):
    @api.doc('Delete Comment')
    def get(self, comment_id):
        """ Delete Spisific Comment """
        comment = delete_a_comment(comment_id)
        return comment
