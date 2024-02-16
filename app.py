# app.py
from flask import Flask
from main import *
app = Flask(__name__)
###

@app.route('/', methods=['GET'])
def home():
    return "Homepage"

@app.route('/contact', methods=['GET'])
def contact():
    return "Contact page"
    
if __name__ == "__main__":
    app.run() | Source: Genelify.com 
