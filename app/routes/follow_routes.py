import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.user import User
from ..models.follow import Follow

bp = Blueprint('follow_bp', __name__, url_prefix='/follows')

@bp.post('/<followed_user_id>')
@jwt_required()
def follow_user(followed_user_id):

    user_id = get_jwt_identity()

    follow_data = {
        "follower_id": user_id,
        "followed_id": followed_user_id
    }

    try:
        new_follow = Follow.from_dict(follow_data)

        db.session.add(new_follow)
        db.session.commit()
    except IntegrityError:
        response = {"message": "User already followed"}
        abort(make_response(response, 409))

    return {"follow": new_follow.to_dict()}

@bp.delete('/<followed_user_id>')
@jwt_required()
def unfollow_user(followed_user_id):

    user_id = get_jwt_identity()

    query = db.select(Follow).where(and_(Follow.follower_id == user_id, Follow.followed_id == followed_user_id))
    follow = db.session.scalar(query)

    db.session.delete(follow)
    db.session.commit()

    return Response(status=204, mimetype='application/json')