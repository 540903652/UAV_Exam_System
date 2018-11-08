import os

from flask_login import LoginManager


class Config:
    SECRET_KEY = '540903652'

    basedir = os.path.abspath(os.path.dirname(__file__))

    # The SQLAlchemy connection string.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '2424911623@qq.com'
    MAIL_PASSWORD = 'vgzpzczgthhediag'
    FLASKY_MAIL_SENDER = '2424911623@qq.com'
    FLASKY_ADMIN = '2424911623@qq.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[UAV_Exam_System]'

