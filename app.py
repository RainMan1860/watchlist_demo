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

@app.route ("/")
def index():
	return render_template("index.html",name=name,movies = movies)

# 使用SQLAlchemy 操作数据库
from flask_sqlalchemy import SQLAlchemy
import os
# 配置数据库变量
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(app.root_path,'data.db')
	# SQLite 的格式值为 sqlite：///数据库文件的绝对地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭对模型修改的监控

db = SQLAlchemy(app) # 初始化扩展，传入程序实例app

# ---创建数据库模型，保存用户信息和电影条目信息----
# ORM 借助python类操作数据库的表
class User(db.Model):
	id 	= db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(20)) # 人名

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

