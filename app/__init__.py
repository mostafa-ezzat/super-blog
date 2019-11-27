from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.post_controller import api as post_ns
from .main.controller.comment_controller import api as comment_ns
from .main.util.dto import LikeDto

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(post_ns)
api.add_namespace(comment_ns)

# This Dtos Api without controller
like_ns = LikeDto.api
api.add_namespace(like_ns)
