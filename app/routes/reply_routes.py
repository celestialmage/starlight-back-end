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

bp = Blueprint('reply_bp', __name__, url_prefix='/replies')

