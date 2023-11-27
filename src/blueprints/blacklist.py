from flask import Blueprint, jsonify, request
from src.commands.add_email import AddEmail
from src.commands.validate_email import ValidateEmail
from src.models.database import db_session

blacklists_blueprint = Blueprint('blacklist', __name__)

@blacklists_blueprint.route('/blacklists', methods = ['POST'])
def add_email():
    json_request = request.get_json()
    result = AddEmail(db_session, json_request,request.headers,request.remote_addr).execute()  
    return jsonify({'msg':result}),201  
 

@blacklists_blueprint.route('/blacklists/<string:email>', methods=['GET'])
def validate_email(email):
    result = ValidateEmail(db_session, request.headers, email).execute()
    return jsonify({'msg':result}),200
  
@blacklists_blueprint.route('/ping', methods=['GET'])
def ping():
    return "Config New Relic UP"
  