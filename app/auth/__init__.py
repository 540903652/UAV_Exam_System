from flask import Blueprint
###导入Blueprint

auth = Blueprint('auth', __name__)

from . import views