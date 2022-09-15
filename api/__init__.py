from flask import Flask, jsonify
from .image.views import image
from .helpers.helpers import set_flask_environment
from .extensions.extensions import cors, swagger, db, ma
from flasgger import LazyJSONEncoder


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
    
    app.register_blueprint(image, url_prefix='/api/v1/image')
    
    app.shell_context_processor({'app': app})
    return app