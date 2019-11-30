from flask_restplus import Namespace, fields
from app.main.util.custome_fields import TimeFormat

# User Marshalling


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='User email address'),
        'username': fields.String(required=True, description='User username'),
        'password': fields.String(required=True, description='User password'),
        'public_id': fields.String(description='User Identifier'),
        'thumbnail': fields.String(description='User Thumbnail')
    })

    user_name = api.model('author', {
        'name': fields.String(required=True, description='user username',
                              attribute='username')
    })

# Authorization Marshalling


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True,
                                  description='The user password')
    })

# Category Marshalling


class CatDot():
    api = Namespace('categories', description='category related operations')
    cat = api.model('cat', {
        'cat': fields.String()
    })

# Like Marshalling


class LikeDto:
    api = Namespace('like', description='Like Related Operations')
    like = api.model('like', {
        'user': fields.Nested(UserDto.user_name, attribute='likes')
    })

# Comment Marshalling


class CommentDto:
    api = Namespace('comment', description='Comment Related Operations')
    comment = api.model('comment', {
        # 'id': fields.Integer(required=True, description='Comment Identifier'),
        # 'post_id': fields.Integer(required=True, description='Post Identifier'),
        # 'user_id': fields.Integer(required=True, description='User Identifier'),
        'body': fields.String(),
        'creation_date': TimeFormat(readonly=True),
    })


CommentDto.rescomment = CommentDto.comment.clone('comment', {
    'reply': fields.Nested(CommentDto.comment)
})

# Post Marshalling


class PostDto:
    api = Namespace('post', description='post related operations')
    post = api.model('post', {
        'title': fields.String(required=True, description='The title'),
        'body': fields.String(required=True, description='The post body'),
        'author': fields.Nested(UserDto.user_name, attribute='user'),
        'categories': fields.List(fields.String()),
        'like': fields.Nested(LikeDto.like),
        'creation_date': TimeFormat(readonly=True)
    })

# Continue Post Marshalling


UserDto.many_user = UserDto.api.clone('user_with_posts', UserDto.user, {
    'post': fields.List(fields.Nested(PostDto.post))
})
