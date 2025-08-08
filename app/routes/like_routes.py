import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.user import User
from ..models.post import Post
from ..models.like import Like

bp = Blueprint('like_bp', __name__, url_prefix='/likes')

@bp.get('')
@jwt_required()
def get_user_likes():

    user_id = get_jwt_identity()

    user = validate_model(User, user_id)

    likes = user.likes

    likes_response = [like.to_dict() for like in likes]

    response = {
        'likes': likes_response
    }

    return response, 200

@bp.post('/<post_id>')
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()

    like_data = {
        'post_id': post_id,
        'user_id': user_id
    }

    try:
        new_like = Like.from_dict(like_data)

        db.session.add(new_like)
        db.session.commit()

    except:
        response = {'message': 'Post already liked'}
        abort(make_response(response, 409))

    return {'like': new_like.to_dict()}

@bp.delete('/<post_id>')
@jwt_required()
def unlike_post(post_id):

    user_id = get_jwt_identity()
    
    query = db.select(Like).where(and_(Like.post_id == post_id, Like.user_id == user_id))
    like = db.session.scalar(query)

    if not like:
        response = {'message': 'Like not found'}
        abort(make_response(response, 404))

    db.session.delete(like)
    db.session.commit()

    return Response(status=204, mimetype='application/json')