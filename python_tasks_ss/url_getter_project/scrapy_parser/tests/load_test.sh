#!/usr/local/bin/bash

curl -d 'source=https://modwsgi.readthedocs.io/en/develop/user-guides/configuration-guidelines.html' 'http://192.168.56.102/urls'
echo '\r\n--------------------------------------------------'
time
curl -d 'source=https://modwsgi.readthedocs.io/en/develop/user-guides.html' 'http://192.168.56.102/urls'
echo '\r\n------------------------------------------------'
time
curl -d 'source=https://httpd.apache.org/docs-project/' 'http://192.168.56.102/urls'
time
#for i in {1..5}; do
#    curl -d 'source=https://www.w3schools.com/cssref/css_selectors.asp' 'http://192.168.56.102/urls'
#    curl -d 'source=http://flask.pocoo.org/docs/1.0/quickstart/' 'http://192.168.56.102/urls'
#    curl -d 'source=https://github.com/Rocckk/my-repo' 'http://192.168.56.102/urls'
#    sleep 1
#done
