import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.post import Post
from ..models.user import User

bp = Blueprint('post_bp', __name__, url_prefix='/posts')

@bp.post('')
@jwt_required()
def create_post():

    user_id = get_jwt_identity()

    request_body = request.get_json()

    request_body["user_id"] = user_id

    request_body = jsonify(request_body)

    new_post = model_from_request(cls=Post, request=request_body)

    user = validate_model(User, user_id)

    user.posts.append(new_post)

    db.session.commit()

    response = {
        "post": new_post.to_dict()
    }

    return response, 201

@bp.delete('/<post_id>')
@jwt_required()
def delete_post(post_id):

    user_id = get_jwt_identity()

    post = validate_model(Post, post_id)

    print(user_id, post.user_id)
    print(type(user_id), type(post.user_id))

    if user_id == post.user_id:
        db.session.delete(post)
        db.session.commit()
    else:
        response = { "message": "user is not the author of this tweet." }
        abort(make_response(response, 403))

    return Response(status=204, mimetype='application/json')


@bp.get('/user/<user_id>')
@jwt_required()
def get_user_posts(user_id):

    user = validate_model(User, user_id)

    posts = [post.to_dict() for post in user.posts]

    response = {
        "posts": posts
    }

    return jsonify(response), 200