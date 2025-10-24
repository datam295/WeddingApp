from flask import Flask
from .routes import main  # or however you set up your Blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
