from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

import os 
from flask import Flask, jsonify
from src.blueprints.blacklist import blacklists_blueprint
from src.errors.errors import ApiError
from src.models.database import Base, engine
from sqlalchemy import inspect


application = Flask(__name__)

application.register_blueprint(blacklists_blueprint)


@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

    
def init_db():
  if not inspect(engine).has_table("blacklist"):
    Base.metadata.create_all(bind=engine)
    
with application.app_context():
  init_db()

