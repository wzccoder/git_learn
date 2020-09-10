#encoding:utf-8
from flask_sqlalchemy import SQLAlchemy
# 目的是：分开models，解决循环引用
db = SQLAlchemy()