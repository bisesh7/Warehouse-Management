from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
jwt = JWTManager(app)

# MongoDB setup
client = MongoClient(app.config['MONGO_URI'])
db = client['warehouse_db']

# Import and register blueprints for routes
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.report_routes import report_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(report_bp, url_prefix='/reports')

if __name__ == "__main__":
    app.run(debug=True)
