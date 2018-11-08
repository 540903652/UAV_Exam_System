from flask import render_template

from app import db, app
from app.auth.form import UserForm
from app.exam import views


@app.route('/')
def index():
    form = UserForm()
    return render_template('auth/index.html', form=form)


db.create_all()
