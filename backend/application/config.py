import os
from datetime import datetime,timedelta


DB_FILE = "database.sqlite3"

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = "sqlite:///" + os.path.join(basedir, DB_FILE)
dbfile = os.path.join(basedir, DB_FILE)

class Config():
    SECRET_KEY = "iusnd"
    SQLALCHEMY_DATABASE_URI = db_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=10)
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CACHE_TYPE='RedisCache'
    CACHE_REDIS_URL='redis://localhost:6379/2'
    CACHE_DEFAULT_TIMEOUT=200
    JWT_SECRET_KEY=SECRET_KEY
    REDIS_URL = "redis://localhost:6379"
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    broker_connection_retry_on_startup = True