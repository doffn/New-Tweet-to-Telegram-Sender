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

def start():
    app.run()
    
if __name__ == "__main__":
    thread_new = threading.Thread(target=start)
    thread_new.start()
