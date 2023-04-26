from api.controllers.public import public_bp
from api.controllers.chat import chat_bp

def register_blueprints(app):
    app.register_blueprint(public_bp)
    app.register_blueprint(chat_bp)