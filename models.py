#encoding:utf-8
from datetime import datetime
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash

# 本函数用于创建各种模型，以便将前端传过来的数据保存到数据库
# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # 主要是实现对用户密码的加密
    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    # 主要实现对用户加密数据的解码，并返回布尔类型数据
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

# 提问模型
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次开始运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author与User模型中的user表单产生关系，questions与author的反向关系，即通过questions可以查看
    # 该作者发表的所有问题
    author = db.relationship('User', backref=db.backref('questions'))

# 回答问题模型
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers'))
    author = db.relationship('User', backref=db.backref('answers'))

