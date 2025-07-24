import requests
from flask import request, jsonify, Blueprint, Response, abort, make_response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, current_user
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

@bp.patch('')
@jwt_required()
def edit_profile():

    pass