from flask import Flask,request,send_file,jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from application.config import Config
from application.models import db
from application.api import api
from application import workers
from application import tasks
from application.cache import cache
from celery.result import AsyncResult
celery=None
app=None
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()
    cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173","http://127.0.0.1:5173"]}})
    api.init_app(app)
    cache.init_app(app)
    jwt = JWTManager(app)
    app.app_context().push()
    celery=workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        broker_connection_retry_on_startup=app.config["CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"]
        )
    celery.Task = workers.FlaskTask
    app.app_context().push()
    app.extensions["celery"] = celery
    app.app_context().push()
    return app,api,celery

app,api,celery = create_app()
@app.route('/export_csv')
def index():
    task = tasks.csv_report()
    return jsonify({'message':'csv file is sent to your email please check'})



if __name__ == '__main__':
    app.run(debug=True,port="8080")
