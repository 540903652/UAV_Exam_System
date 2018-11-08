import uuid

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


def gen_id():
    return uuid.uuid4().hex.replace('-', '')


class BaseModel():
    def save(self):
        db.session.save(self)

    def delete(self):
        db.session.delete(self)

    def update(self):
        db.session.update(self)



class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()

        return True

    def __repr__(self):
        return '<User %r>' % self.username


class Type(db.Model):
    """
        :类型
        :param  id  类型id
        :param  name  类型名
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    libs = db.relationship('Library')

    def __repr__(self):
        return self.name


class Library(db.Model):
    """
        :试题集
        :param id  试题id
        :param tid  试题类型
        :param topic  试题内容
        :param option_fir  选项1
        :param option_sec 选项2
        :param option_thd 选项3
        :param answer 答案
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, db.ForeignKey("type.id"), name='type')
    type = db.relationship('Type')
    content = db.Column(db.String(564))
    optionFir = db.Column(db.String(564))
    optionSec = db.Column(db.String(564))
    optionThd = db.Column(db.String(564))
    answer = db.Column(db.String(5))
    finished = db.relationship('FinishedCollection')


class MistakesCollection(db.Model):
    """
        :错题集
        :param id  错题id
        :param libId  试题id
        :param lib  试题
        :param uid  所属用户id
        :param owner 所属用户
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libId = db.Column(db.Integer, db.ForeignKey("library.id"))
    lib = db.relationship('Library')
    uid = db.Column(db.String(32), db.ForeignKey('user.id'))
    owner = db.relationship('User')


class FinishedCollection(db.Model):
    """
        :完成题集
        :param id  id
        :param libId  试题id
        :param lib  试题
        :param uid  所属用户id
        :param owner 所属用户
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libId = db.Column(db.Integer, db.ForeignKey("library.id"))
    lib = db.relationship('Library')
    uid = db.Column(db.String(32), db.ForeignKey('user.id'))
    owner = db.relationship('User')


class Records(db.Model):
    """
        :测试记录
        :param id  记录id
        :param right_num  正确数
        :param wrong_num  错误数
        :param total_num  总数
        :param create_date   答题时间
        :param total_time   答题用时
        :param uid   所属用户id
        :param owner   所属用户
        :param
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship('Type')
    right_num = db.Column(db.Integer)
    wrong_num = db.Column(db.Integer)
    total_num = db.Column(db.Integer)
    remainder = db.Column(db.Integer)
    degree = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    uid = db.Column(db.String(32), db.ForeignKey("user.id"))
    owner = db.relationship('User')

    def __init__(self, type,owner,right_num=0,wrong_num=0,degree=0,total_titme=0):
        self.total_titme = total_titme
        self.degree = degree
        self.wrong_num = wrong_num
        self.right_num = right_num
        self.owner = owner
        self.total_num = Library.query.filter_by(tid=type.id).count()
        self.type = type
        self.remainder = Library.query.filter_by(tid=type.id).count()


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(32), db.ForeignKey("user.id"))
    owner = db.relationship('User')
    score = db.Column(db.Integer)
    date = db.Column(db.Float)
    total_time = db.Column(db.Integer)
