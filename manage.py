#encoding:utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from zlktqa import app
from models import User, Question, Answer
# 报错：AssertionError: The sqlalchemy extension was not registered to the current application.
# Please make sure to call init_app() first. 解决办法如下：
# 该函数用于将本地数据上传到数据库中
db.init_app(app)

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# 将模型映射到数据库的命令行：
# Python manage.py db init 用于初始化迁移的环境
# Python manage.py db migrate 用于生成迁移文件
# python manage.py db upgrade 用于将迁移文件映射到数据库