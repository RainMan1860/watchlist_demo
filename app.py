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

@app.route("/")
def hello():
	return  "hello"

@app.route('/test')
def test_url_for():
	print(url_for('hello'))
	print(url_for("user_page",name='xy'))
	print(url_for('test_url_for'))
	return 'Test page'
