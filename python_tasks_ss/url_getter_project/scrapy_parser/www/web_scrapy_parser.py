import json
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_paginate import Pagination
from db_connector import FlaskDbConnector


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/urls', methods=['GET','POST'])
def handle_form():
    if request.method == "GET" and not request.args:
        return redirect(url_for('index'))
    elif request.method == "POST":
        source = request.form['source']
        with FlaskDbConnector(source, 25, 0) as db_conn:
            try:
                urls_counts, present, top, total = db_conn.handle_source()
            except TypeError:
                value = db_conn.handle_source()
                if isinstance(value, int):
                    if value == 204:
                        return render_template('result.html', source=source)
                elif value < 500:
                    return "Client error occurred", value
                elif value >= 500:
                    return "Server error occurred", value
            pagination = Pagination(page=1, per_page=25, total=total,
                                    record_name="urls", format_total=True,
                                    format_number=True,
                                    href="urls?page={0}&num={1}&source={2}\
#table_top".format('{0}',total, source))
            return render_template('result.html', source=source,
                                                      urls=urls_counts,
                                                      present=present, top=top,
                                                      total=total,
                                                      pagination=pagination,
                                                      )

    elif request.method == "GET" and request.args:
        source = request.args['source']
        page_num = int(request.args['page'])
        per_page = 25
        total_num = request.args['num']
        offset = per_page * page_num - per_page
        with FlaskDbConnector(source, per_page, offset) as db_conn:
            try:
                urls_counts, present, top, total = db_conn.handle_source()
            except TypeError:
                value = db_conn.handle_source()
                if isinstance(value, int):
                    if value == 204:
                        return render_template('result.html', source=source)
                    elif value < 500:
                        return "Client error occurred", value
                    elif value >= 500:
                        return "Server error occurred", value
            pagination = Pagination(page=page_num, per_page=per_page,
                                    total=int(total_num), record_name="urls",
                                    format_total=True, format_number=True,
                                    href="urls?page={0}&num={1}&source={2}\
#table_top".format('{0}',total_num, source))
            return render_template('result.html', source=source,
                                                      urls=urls_counts,
                                                      present=present, top=top,
                                                      total=total_num,
                                                      pagination=pagination)


@app.route('/top<number>', methods=['GET'])
def get_tops(number):
    with FlaskDbConnector(top=number) as db_conn:
        result = db_conn.get_top_total()
    return render_template('top.html', result=result)

@app.route('/suggest', methods=['POST'])
def autocomplete():
    source_part = request.form['entered']
    with FlaskDbConnector(source_part) as db_conn:
        suggestions = db_conn.suggest_source()
        print(suggestions)
    if suggestions:
        return json.dumps(suggestions)
    return json.dumps([])

@app.route('/loaderio-f13efd02e5ea34525c3c97794a18832a/', methods=['POST', 'GET'])
def token():
    print('loaderio-f13efd02e5ea34525c3c97794a18832a/')
    return send_file('token.txt')

