import requests
from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required
from .route_utils import validate_model, model_from_request
from ..db import db
from ..models.user import User

bp = Blueprint('user_bp', __name__, url_prefix='/users')

# @jwt_required
@bp.post('')
def create_user():

    print("Beginning Create User")

    new_user = model_from_request(cls=User, request=request)

    print("Checking Username Availibility")

    query = db.select(User).where(User.username == new_user.username)

    print("Constructed new User")

    db.session.add(new_user)
    db.session.commit()

    print("Committed database")

    return {"user": new_user.to_dict()}, 201
