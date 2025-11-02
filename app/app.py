from flask import Flask
from .routes import main  # or however you set up your Blueprint
import os

if os.getenv("GOOGLE_CREDENTIALS_JSON"):
    with open("service-account.json", "w") as f:
        f.write(os.environ["GOOGLE_CREDENTIALS_JSON"])

def create_app():

    app = Flask(__name__)
    app.secret_key = 'replace-this-with-a-strong-secret-key'  # Set a secure, random value in production
    app.register_blueprint(main)
    return app


# Standalone app instance for running directly
app = Flask(__name__)
app.secret_key = 'replace-this-with-a-strong-secret-key'  # Set a secure, random value in production
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
