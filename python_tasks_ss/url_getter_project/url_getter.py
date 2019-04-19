"""this module's purpose is to parse a webpage and grab all the URLS which are
on that webpage and write it to a file"""


import requests
from html.parser import HTMLParser
import re
import argparse


class Page_Handler(HTMLParser):
    """this class accepts a URL and looks for links in it"""
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.link_tags = ['a', 'applet', 'base', 'bgsound', 'blockquote',
                          'body', 'button', 'command', 'del', 'embed', 'form',
                          'frame', 'head', 'html', 'iframe', 'img', 'input',
                          'ins', 'isindex', 'link', 'object', 'q', 'script',
                          'source', 'table', 'td', 'th', 'video']
        self.link_attrs = ['archive', 'codebase', 'href', 'src', 'cite', 
                           'background', 'formaction', 'icon', 'pluginspage',
                           'action', 'profile', 'manifest', 'xmlns', 'lowsrc',
                           'classid', 'data']
        self.targ_file = 'urls.txt'

    def get_urls(self):
        r = requests.get(self.url)
        if r.status_code >= 200 and r.status_code < 300:
            self.feed(r.text)

    def write_to_file(self, link):
        with open(self.targ_file, 'a') as f:
            f.write(link + '\n')

    def handle_starttag(self, tag, attrs):
        if tag in self.link_tags:
            for attr in attrs:
                if attr[0] in self.link_attrs and attr[1].startswith('http'):
                    print(attr[1])
                    self.write_to_file(attr[1])

    def handle_decl(self, decl):
        # some links could appear in DOCTYPE declaration too
        if 'http' in decl:
            print(decl[decl.find('http'):len(decl)-1])
            self.write_to_file(decl[decl.find('http'):len(decl)-1])

    def handle_comment(self, data):
        # some links could appear in comments
        while 'http' in data:
            pattern = r'http[^\s]+'
            match = re.search(pattern, data).group()
            print(match)
            self.write_to_file(match)
            data = data.replace(match, '', 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', help='the url of the webpage you would like to\
            get urls from')
    args = parser.parse_args()
    if args.url:
        h = Page_Handler(args.url)
        html = h.get_urls()
    else:
        print('you did not provide any URL to look for')

if __name__ == '__main__':
    main()
