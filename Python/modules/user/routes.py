from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from modules.user.services import UserService
from logger import setup_logger
import json

def create_user_blueprint(user_service: UserService):
    user_bp = Blueprint('user', __name__)
    logger = setup_logger(__name__)

    @user_bp.route('/login', methods=['POST'])
    def get_user():
        try:
            data = request.get_json()
            access_token, refresh_token = user_service.get_user(data)

            return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 401

    @user_bp.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():

        current_user_id = get_jwt_identity()  # Retorna '1' como string
        print(">>> current_user_id:", current_user_id)

        new_access_token = create_access_token(identity=current_user_id)
        return jsonify({"access_token": new_access_token}), 200
    
    @user_bp.route('/create', methods=['POST'])
    def create():
        try:
            data = request.get_json()
            json = user_service.create(data)

            if json:
                return jsonify({"success": "Usuario criado com sucesso!"}), 200
            return jsonify({"error": "Nao foi possivel criar usuario!"}), 500

        except ValueError as e:
            return jsonify({"error": str(e)}), 401

        

    return user_bp
    