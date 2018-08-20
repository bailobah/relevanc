import os
import settings
from logger import Logger
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

from api.controllers.dataset_controller import ns as doc_dataset_namespace
from api.controllers.trace_controller import ns as doc_trace_namespace

from api.restplus import api
from database import db

app = Flask(__name__)
log = Logger.log

def configure_app(flask_app):
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    #flask_app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

def init(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.namespaces.clear() 
    api.add_namespace(doc_dataset_namespace)
    api.add_namespace(doc_trace_namespace)
 
    flask_app.register_blueprint(blueprint)

    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()

def run():
    init(app)

    log.info('='*20)
    log.info('Starting development server at http://{}:{}/api/'\
        .format(settings.FLASK_SERVER_NAME,os.environ.get('PORT', settings.FLASK_SERVER_PORT)))
    app.run(debug=settings.FLASK_DEBUG,\
             host=os.environ.get(settings.FLASK_SERVER_NAME,'0.0.0.0'),\
             port=int(os.environ.get('PORT', settings.FLASK_SERVER_PORT))\
         )

if __name__ == "__main__":
    run()

