from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from exts import db
from models import User, Question, Answer
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
# flask的工作框架：MTV 数据库+模板+视图函数
# 知了课堂主页
@app.route('/')
def index():
    # 将问答数据渲染到网站首页
    # context()函数用法,上下文钩子函数用于在登录后的界面显示类似知乎的问答界面
    context = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    # 渲染登录后首页显示的内容
    return render_template('index.html', **context)

# 用户登录功能的视图函数
@app.route('/login/', methods=["GET", "POST"])
def login():
    # 从服务器获得登录界面，所以使用“GET”方法
    if request.method == "GET":
        return render_template("login.html")
    # 否则为“POST”方法，向服务器中上传数据，会对服务器产生影响
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        # 在数据库中搜索当前登录的用户是否存在
        user = User.query.filter(User.telephone == telephone).first()
        # check_password()函数用于解析被加密的用户密码，返回布尔型数据
        if user and user.check_password(password):
            # 将 user_id 存入session，然后服务器将cookie数据发送到浏览器保存，提高用户访问的速度
            session['user_id'] = user.id
            # 如果想31天内自动登录，则长期保存密码
            session.permanent = True
            return redirect(url_for("index"))
        else:
            return u"用户名或密码错误，请重新输入"

# 用户注册功能的视图函数
@app.route('/register/', methods=["GET", "POST"])
def register():
    # “GET“方法，从服务器返回渲染后的注册界面
    if request.method == "GET":
        return render_template("register.html")
    # “POST”方法，向服务器上传数据
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # 手机号码验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已经被注册，请更换手机号码！'
        else:
            # 对输入密码是否一致进行验证
            if password1 != password2:
                return u'两次密码输入不一致，请重新输入'
            else:
                # 将用户的注册信息上传到服务器的User模型中保存
                user = User(telephone=telephone, username=username, password=password1)
                # 向数据库中添加数据
                db.session.add(user)
                # 上传事物表单
                db.session.commit()
                # 重定向到登录界面
                return redirect(url_for("login"))

# 用户注销功能的视图函数
@app.route("/logout")
def logout():
    # 注销登录的几种方式
    # del session['user_id']
    # session.clear()
    session.pop('user_id')
    return redirect(url_for('login'))

# 知了课堂问答界面实现的视图函数
@app.route("/detail/<question_id>/")
def detail(question_id):
    # 从数据库中查询到具体某个问题的表单
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)

# 添加问题回复的视图函数
@app.route("/add_answer/", methods=["POST"])
# login_required 装饰函数用于验证用户是否登录，若未登录，则跳转到登录界面
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)

    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    # user_id = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    db.session.add(answer)
    db.session.commit()
    # 重定向到回答问题的界面
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {"user": user}
    # return {}

# 用户发帖的功能实现，其中包括用户登录验证
@app.route("/question", methods=["GET", "POST"])
@login_required
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        # 重定向到首页
        return redirect(url_for('index'))

# 知了课堂搜索功能实现
@app.route("/search/")
def search():
    q = request.args.get("q")
    #   查找的关键字要么在title，要么在content
    #   用或运算符进行查找
    #   或运算过滤
    condition = or_(Question.title.contains(q), Question.content.contains(q))
    questions = Question.query.filter(condition).order_by(Question.create_time.desc()).all()

    return render_template('index.html', questions=questions)

# 辅助函数，在执行任何一个视图函数之前首先运行下面的代码
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

if __name__ == '__main__':
    app.run()
