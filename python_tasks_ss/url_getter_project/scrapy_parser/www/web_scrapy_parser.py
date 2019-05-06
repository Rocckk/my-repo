from flask import Flask, render_template, request
from db_connector import FlaskDbConnector


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        source = request.form['url']
        with FlaskDbConnector(source) as links:
            if links:
                urls = links
                return render_template('result.html', source=source, urls=urls) 
            else: 
                print('no links were found')
                return render_template('result.html', source=source)
