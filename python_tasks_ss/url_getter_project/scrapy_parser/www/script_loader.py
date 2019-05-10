"""
this module loads the shell scrip which launches the scrapy_parser project
and scrapes the links from a given source web pave
"""
import os
import subprocess

def run(source):
    '''
    This function runs the project's scrapy_parser script to scrape a new source
    URL and update the Db with scraped links
    params:
    source = str, the source URL which is scraped
    returns:
    True - if the script ran successfully, otherwise - False
    '''
    pwd = subprocess.run("pwd", shell=True, stdout=subprocess.PIPE,
                         encoding='utf-8')
    if not pwd.stdout.endswith('www'):
        os.chdir('www')
    proc = subprocess.run("../bin/scrapy_parser.sh '{}'".format(source),
                          shell=True)
    if proc.returncode == 0:
        return True