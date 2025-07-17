from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from db_functions import Database
from datetime import timedelta 
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from flask_cors import CORS


app = Flask(__name__)
load_dotenv()
CORS()
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['PORT'] = os.getenv('PORT')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECERT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

database_instance = Database()

jwt = JWTManager(app)

@app.route("/", methods=['GET'])
def home():
    #health check endpoint
    return jsonify({"message" : "hello, sever started successfully"}), 200

@app.route("/register", methods=['POST'])
def register_user():
    #endpoint to register new user
    if(request.is_json):
        data = request.get_json()
        database_response = database_instance.create_user(data["operator_id"], data["operator_name"], data["password"], data["mobile_number"])
        
        if(database_response):
            return jsonify({"message" : "data_inserted_successfully", "status" : 1}), 200

@app.route("/login", methods=['POST'])
def login_user():
    #endpoint to login user and create access token
    if(request.is_json):
        data = request.get_json()
        operator_id = data["operator_id"]
        password = data["password"]

        is_valid_cred = database_instance.fetch_user(operator_id, password)
        if(is_valid_cred):
            access_token = create_access_token(identity=str(is_valid_cred))
            return jsonify({"access_token" : access_token}), 200
        else:
            return jsonify({"message": "user_not_found"}), 404
        
# Protected Route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"user_id": current_user})


if __name__ == "__main__":
    #driver code

    app.run(host="0.0.0.0", port=app.config['PORT'], debug=True)