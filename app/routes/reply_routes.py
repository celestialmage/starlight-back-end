import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.post import Post
from ..models.user import User
from ..models.user import Follow
from ..models.reply import Reply

bp = Blueprint('reply_bp', __name__, url_prefix='/replies')

@bp.post('/post/<post_id>')
@jwt_required()
def create_reply(post_id):

    user_id = get_jwt_identity()

    request_body = request.get_json()
    request_body['user_id'] = user_id
    request_body['post_id'] = post_id
    request_body = jsonify(request_body)

    new_reply = model_from_request(cls=Reply, request=request_body)

    post = validate_model(Post, post_id)

    post.replies.append(new_reply)
    db.session.commit()

    response = {
        'reply': new_reply.to_dict()
    }

    return response, 201

@bp.delete('/<reply_id>')
@jwt_required()
def delete_reply(reply_id):

    user_id = get_jwt_identity()

    reply = validate_model(Reply, reply_id)

    if not reply:
        response = { 'message': 'reply does not exist' }
        abort(make_response(response, 404))

    if user_id == reply.user_id:
        db.session.delete(reply)
        db.session.commit()
    else:
        print(user_id, reply.user_id)
        response = { 'message': 'user is not the author of this reply' }
        abort(make_response(response, 403))

    return Response(status=204, mimetype='application/json')

@bp.get('/post/<post_id>')
@jwt_required()
def get_post_replies(post_id):

    post = validate_model(Post, post_id)

    replies = post.replies

    replies_response = [reply.to_dict() for reply in replies]

    response = {
        'replies': replies_response
    }

    return response, 200