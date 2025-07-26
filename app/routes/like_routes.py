import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.user import User
from ..models.post import Post
from ..models.like import Like

bp = Blueprint('like_bp', __name__, url_prefix='/likes')

@bp.post('/<post_id>')
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()

    like_data = {
        "post_id": post_id,
        "user_id": user_id
    }

    try:
        new_like = Like.from_dict(like_data)

        db.session.add(new_like)
        db.session.commit()

    except:
        response = {"message": "Post already liked"}
        abort(make_response(response, 409))

    return {"like": new_like.to_dict()}