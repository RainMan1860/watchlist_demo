# version 1
from flask import Flask
from flask import url_for
app = Flask(__name__)

# 装饰器的参数称为URL规则
# 可以在URL里面定义变量
@app.route('/user/<name>')
def user_page(name):
	#return("欢迎来到我的 Watch list!")
	#print('User name is %s' % name)
	return 'User name is %s' % name +'<h1>hello again</h1> <img src ="http://watchlist.helloflask.com/static/images/totoro.gif" > '


@app.route('/test')
def test_url_for():
	print(url_for('hello'))
	print(url_for("user_page",name='xy'))
	print(url_for('test_url_for'))
	return 'Test page'

name = "Grey Li"
movies = [
	{"title":"My Neighbor Totoro","year":"1988"},
	{"title":"Dead Poets Society","year":"1989"},
	{"title":"A Perfect World","year":"1993"},
	{"title":"Leon","year":"1994"},
	{"title":"Mahjong","year":"1996"},
	{"title":"Swallowtail Butterfly","year":"1996"},
	{"title":"King of comedy","year":"1999"},
	{"title":"Devils on the Doorstep","year":"1999"},
	{"title":"Wall-E","year":"2008"},
	{"title":"The pork of Music","year":"2012"},
]

from flask import render_template

## @app.route ("/")
## def index():
##	return render_template("index.html",name=name,movies = movies)

# 使用SQLAlchemy 操作数据库
from flask_sqlalchemy import SQLAlchemy
import os
# 配置数据库变量
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(app.root_path,'data.db')
	# SQLite 的格式值为 sqlite：///数据库文件的绝对地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭对模型修改的监控

db = SQLAlchemy(app) # 初始化扩展，传入程序实例app

# ---创建数据库模型，保存用户信息和电影条目信息----
from werkzeug.security import generate_password_hash,check_password_hash
# ORM 借助python类操作数据库的表
#from flask_login import UserMixin
# 继承Flask-Login 提供的Usermaixin类,让User类拥有用于判断认证状态的属性和方法
#常用的有is_authenticated属性，
#class User(db.Model,UserMixin):
#	id 	= db.Column(db.Integer,primary_key = True)
#	name = db.Column(db.String(20)) # 权限
#	username =db.Column(db.String(20)) #用户名
#	password_hash =db.Column(db.String(128))#散列值

#	def set_password(self,password):
#		self.password_hash = generate_password_hash(password) #用来获得用户输入的密码，接受密码作为参数

#	def validate_password(self,password):
# 		self.check_password_hash(self.password_hash,password)

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)



class Movie(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title =db.Column(db.String(60)) #电影标题
	year =db.Column(db.String(4)) # 电影年份
#---------------------------------------------------



# --自定义命令 initdb ,自动执行创建数据库表的操作--------
import click
@app.cli.command() # 注册为命令
@click.option('--drop',is_flag=True ,help='create after drop')
def initdb(drop):
	if drop:
		db.drop_all()
	db.create_all()
	click.echo('Initialized database.') #输出提示信息
#-------------------------------------------------

@app.route('/db')
def process():
	user   = User.query.first() #读取用户记录
	movies = Movie.query.all() #读取所有电影记录
	return  render_template('index.html',user=user,movies=movies)

#----------------------------------------------------

# 定义 forge 命令 把所有虚拟数据添加到数据库里面
import click
@app.cli.command()
def forge():
	#b.create_all()  #把生成的数据加入数据库中
	myname = 'xy'
	movies_list = [
	{"title":"My Neighbor Totoro","year":"1988"},
	{"title":"Dead Poets Society","year":"1989"},
	{"title":"A Perfect World","year":"1993"},
	{"title":"Leon","year":"1994"},
	{"title":"Mahjong","year":"1996"},
	{"title":"Swallowtail Butterfly","year":"1996"},
	{"title":"King of comedy","year":"1999"},
	{"title":"Devils on the Doorstep","year":"1999"},
	{"title":"Wall-E","year":"2008"},
	{"title":"The pork of Music","year":"2012"},]
	user = User(name=myname)
	db.session.add(user)
	for m  in movies_list:
		movie_object = Movie(title=m['title'],year = m['year'])
		db.session.add(movie_object)
	db.session.commit()
	click.echo('done!')

# ----------------第一次-自定义错误页面------------------
#如果访问一个不存在的url，flask 会自动返回一个404
#错误相应，默认的错误页面非常简陋
#建立一个404.html 错误模板页面
#装饰器注册一个错误处理函数，当404错误发生时
#page_not_fond()函数被触发，返回值作为响应主体（渲染好的模板）返回给客户端

#-

@app.errorhandler(404)
def page_not_fond(e): #要传入的错误代码
	user = User.query.first()
	return render_template('404.html',user=user),404 # 返回渲染好的模板和404状态码

#------------  第二次-自定义错误处理页面，增加模板上下文处理哈函数----

#使用app.context_procesor 装饰器注册一个模板上下文函数
# 函数返回变量dict(user=user)将统一注入到每一个模板的上下文中，因此可以直接在模板中使用user变量
@app.context_processor #模板上下文函数
def inject_user():
	user = User.query.first()
	return dict(user=user)

# 因为使用了上下文，为每个模板导入了user变量，下面修改路由中的user =user
@app.errorhandler(404) #装饰器 errhander
def page_not_fond(e): #要传入的错误代码
	#user = User.query.first()
	#return render_template('404.html',user=user),404 # 返回渲染好的模板和404状态码
	return render_template('404.html'),404 # 返回渲染好的模板和404状态码

#修改路由
#@app.route ("/")
#def index():
#	#return render_template("index.html",name=name,movies = movies)
#	movies = Movie.query.all()
#	return render_template('index.html',movies = movies)

#修改装饰器
from  flask import request
from flask import flash
from flask import redirect
app.config['SECRET_KEY'] = 'dev'
from flask_login import login_required ,current_user# 过滤

@app.route('/',methods=['GET','POST'])
def index():
	if	request.method == 'POST':
		if not current_user.is_authenticated: #过滤未授权用户
			return redirect(url_for('index'))
		title = request.form.get('title')
		year =	request.f2orm.get('year')
		if not title or not year or len(year)>4 or len(title)>60:
			flash('Invalid input.')
			return redirect(url_for('index'))
		movie = Movie(title=title,year=year)
		db.session.add(movie)
		db.session.commit()
		flash('Item created')
		return  redirect(url_for('index'))
	#return render_template("index.html",name=name,movies = movies)
	movies = Movie.query.all()
	return render_template('index.html',movies = movies)


@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	if  request.method == 'POST':
		title = request.form['title']
		year = request.form['year']

		if  not title or not year  or len(year)>4 or len(title)>60:
			flash('Invalid input')
			return redirect(url_for('edit',movie_id =movie_id))
		movie.title = title
		movie.year = year
		db.session.commit()
		flash('Item updated')
		return redirect(url_for('index'))
	return render_template('edit.html',movie = movie)

@app.route('/movie/delete/<int:movie_id>',methods =['POST'])
@login_required
def delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash('Item deleted')
	return redirect(url_for('index'))


# 创建管理员账户
import click
@app.cli.command()
@click.option('--username',prompt=True ,help = 'The username used to login')
@click.option('--password',prompt=True ,hide_input=True, confirmation_prompt=True, help='The password to login')
def admin(username,password):
	''' create admin user'''
	db.create_all()
	user = User.query.first()
	if user is not None:
		click.echo('updating uer ') #默认只有一个管理员用户，只需用户名和密码
		user.username = username
		user.set_password(password)
	else:
		click.echo('Creating user...')#如果没有用户，则创建管理员账户
		user = User(username = username,name='Admin')
		user.set_password(password)
		db.session.add(user)
	db.session.commit()
	click.echo('Done')

# 使用flask-login 第3方库，实现用户认证

from flask_login import LoginManager

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
	user = User.query.get(int(user_id))
	return user

#登录用户 使用Flask-Login 提供的login_user()函数实现，
# 需要传入用户模型类对象作为参数。
#from flask_login import login_user
#@app.route('/login',methods =['GET','POST'])
#def login():
#	if request.method == 'POST':
#		username = request.form['username']
#		password = request.form['password']
#
#		if not username or not password:
#			flash('Invalid input')
#			return redirect(url_for('login'))
#
#		user = User.query.first()
#		if username == user.username and user.validate_password(password):
#			login_user(user)
#			return redirect(url_for('index'))
#		flash("Invalid username or password")
#
#		return render_template('login.html')

from flask_login import login_user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

# 登出
from flask_login import  login_required,logout_user
@app.route('/logout')
@login_required #用于视图保护
def logout():
	logout_user()
	flash('Goodbye')
	return redirect(url_for('index'))


# 认证保护
# 1 视图保护 2 内容 保护

# 视图保护
# 未登录用户不能执行下面的操作
# 访问编辑界面，# 访问设置页面 # 执行注销操作#执行删除操作 # 执行添加新条目操作
# 对于不允许未登录用户 访问的视图，只需要为视图函数添加一个
#

#添加了@login_required 装饰器后，未登录的用户访问未授权的url，
#Flask-login会把用户重新定向到登录页面，并显示一个错误提示。为了
#让这个重定向操作正确执行，我们还需要把以下login_manager.login_view的值
#设置为程序登录视图的端点（函数名）
login_manager.login_view = 'login'


## 设置页面，支持修改用户的名字
## 包括/settings 路由，setting()路由函数，setting.html页面模板

from flask_login import login_required,current_user

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
	if request.method =="POST":
		name = request.form['name']

		if not name or len(name)>20:
			flash('Invalid input')
			return redirect(url_for('settings'))
		current_user.name = name
		db.session.commit()
		flash('Settings updated.')
		return redirect(url_for('index'))
	return render_template('settings.html')


#模板内容保护
#不能对未登录用户显示下列内容
#创建新条目表单
#编辑按钮
#删除按钮











