from flask import Flask, jsonify
from .helpers.helpers import set_flask_environment
from .extensions.extensions import cors, swagger, db, ma, migrate
from flasgger import LazyJSONEncoder
from .auth.views import auth
from .user.views import user

def create_app(script_info=None):
    """Create the flask application."""
    
    app = Flask(__name__)
    
    set_flask_environment(app)
    
    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Check if application is up."""
        return jsonify({'Hello': 'from the image processing service'}), 200
    
    cors.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(user, url_prefix='/api/v1/user')
    
    app.shell_context_processor({'app': app})
    return app