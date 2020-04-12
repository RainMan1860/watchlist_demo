# version 1
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	return("hi,Welcome to My Watch list!")