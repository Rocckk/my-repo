#!/usr/local/bin/bash

curl -d 'https://www.w3schools.com/cssref/css_selectors.asp' 'http://192.168.56.102/urls'
echo '----------------------------------------------------'
curl -d 'source=http://flask.pocoo.org/docs/1.0/quickstart/' 'http://192.168.56.102/urls'
echo '----------------------------------------------------'
curl -d 'https://github.com/Rocckk/my-repo' 'http://192.168.56.102/urls'                
#for i in {1..5}; do
#    curl -d 'https://www.w3schools.com/cssref/css_selectors.asp' 'http://192.168.56.102/urls'
#    curl -d 'source=http://flask.pocoo.org/docs/1.0/quickstart/' 'http://192.168.56.102/urls'
#    curl -d 'https://github.com/Rocckk/my-repo' 'http://192.168.56.102/urls'
#    sleep 1
#done
