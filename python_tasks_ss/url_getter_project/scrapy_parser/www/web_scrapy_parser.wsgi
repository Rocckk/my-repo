activate_this='/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_getter_project/scrap_venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from web_scrapy_parser import app as application

