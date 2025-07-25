import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.user import User

bp = Blueprint('user_bp', __name__, url_prefix='/users')

@bp.post('')
@jwt_required()
def create_user():

    new_user = model_from_request(cls=User, request=request)

    query = db.select(User).where(User.username == new_user.username)
    guy = db.session.scalars(query)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as error:
        response = { "message": f"Username {new_user.username} is already taken." }
        abort(make_response(response, 409))

    return {"user": new_user.to_dict()}, 201

@bp.get('')
@jwt_required()
def get_user():

    user_id = get_jwt_identity()

    user = validate_model(User, user_id)

    response = {
        "user": user.to_dict()
    }

    return response, 200

@bp.patch('')
@jwt_required()
def edit_profile():

    user_token = get_jwt_identity()

    request_stuff = request.get_json()

    edited_profile = request_stuff

    user = validate_model(User, user_token)

    user.edit_profile(edited_profile)

    db.session.commit()

    return { "user": user.to_dict() }, 200