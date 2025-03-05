from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
import argparse
from flask_jwt_extended import JWTManager

from database import DatabaseFactory

from modules.user.repositories import UserRepository
from modules.user.routes import create_user_blueprint
from modules.user.services import UserService
from flasgger import Swagger

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:4200", "http://seu-site.com"]}}, supports_credentials=True)

    app.config['JWT_SECRET_KEY'] = 'QAJPzrZz6nHiI9qKnlgojGzP2'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  # 15 minutos
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 dia

    jwt = JWTManager(app)

    app.config['SWAGGER'] = {
        'title': 'Hydra API',
        'uiversion': 3,
        'description': 'Documentação da API Hydra',
        'specs_route': "/swagger/"
    }
    Swagger(app)

    parser = argparse.ArgumentParser()
    db_factory = DatabaseFactory()
    
    api = Blueprint('api', __name__, url_prefix='/api')

    user_repository = UserRepository(db_factory)
    user_service = UserService(user_repository)
    user_bp = create_user_blueprint(user_service)
    api.register_blueprint(user_bp, url_prefix='/user')

    

    @api.route('/status', methods=['GET'])
    def status():
        return jsonify({"status": "API is running", "version": "v1"}), 200
    

    app.register_blueprint(api, url_prefix='/api')

    parser.add_argument('--mode', default='production', \
                        help='App mode: "developer" or "production"', \
                        required=True)
    args = parser.parse_args()
    app_debug = args.mode

    if app_debug.lower() == 'developer':
        print(' * Running: Flask Development...')
        app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=True)

    elif app_debug.lower() == 'production':
        print(' * Running:  Production...')
        app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False)

    else:
        print('Invalid app mode. Use "developer" or "production".')
