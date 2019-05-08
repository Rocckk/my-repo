from flask import Flask, render_template, request, make_response
from db_connector import FlaskDbConnector


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        source = request.form['url']
        with FlaskDbConnector(source) as value:
            if value:
                if isinstance(value, int):
                    if value == 204:
                        return render_template('result.html', source=source)
                    elif value < 500:
                        return "Client error occurred", value
                    elif value >= 500:
                        return "Server error occurred", value
                urls = value
                return render_template('result.html', source=source, urls=urls)
