import requests
from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .route_utils import validate_model
from ..models.user import User
from werkzeug.exceptions import HTTPException

bp = Blueprint('api_bp', __name__, url_prefix='/api')

def verify_google_token(id_token):
    resp = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': id_token})
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data if data.get('email_verified') else None

@bp.get('')
def send_whatever():
    return {
        "message": "hey guys it's me"
    }

@jwt_required
@bp.post('/login')
def login():

    id_token = request.json.get('credential')
    google_user = verify_google_token(id_token)

    if not google_user:
        return jsonify(msg='Invalid Google token'), 401

    user_id = google_user['sub']

    user_found = True

    try:
        user = validate_model(User, user_id)
    except HTTPException:
        user_found = False
        
    access = create_access_token(identity=user_id)
    refresh = create_refresh_token(identity=user_id)
    return jsonify(access_token=access, refresh_token=refresh, user_found=user_found)

@bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_token)