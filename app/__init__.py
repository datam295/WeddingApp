from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.secret_key = 'replace-this-with-a-strong-secret-key'  # Set a secure, random value in production

    # Import and register blueprints (routes)
    from .routes import main
    app.register_blueprint(main)

    return app
