#encoding:utf-8
import os
import pymysql

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa_demo'
USERNAME = 'root'
PASSWORD = ''
# DB_URI 的坑是：utf8,中间一定不能加‘-’！！！！
# 否则报错AttributeError: 'NoneType' object has no attribute 'encoding'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = False