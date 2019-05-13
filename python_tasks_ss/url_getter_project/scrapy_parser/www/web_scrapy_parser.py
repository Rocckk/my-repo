from flask import Flask, render_template, request, redirect, url_for
from db_connector import FlaskDbConnector


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/send', methods=['GET','POST'])
def handle_form():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        source = request.form['source']
        with FlaskDbConnector(source) as value:
            if value:
                if isinstance(value, int):
                    if value == 204:
                        return render_template('result.html', source=source)
                    elif value < 500:
                        return "Client error occurred", value
                    elif value >= 500:
                        return "Server error occurred", value
                urls, present, top = value
                return render_template('result.html', source=source,
                                                      urls=urls,
                                                      present=present, top=top)
