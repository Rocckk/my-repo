"""this module's purpose is to parse a webpage and grab all the URLS which are
on that webpage and write it to a file"""


import requests
from html.parser import HTMLParser
import re
import argparse


class Page_Handler(HTMLParser):
    """
    this class accepts a URL and looks for links in it. once a link is
    found - it is written to a file urls.txt which is created in the same
    directory as the script
    """
    def __init__(self, url):
        """
        the constructor of the class: it initializes the instance variables
        needed for program:
        params:
        url - str, the URL of the webpage which is being parsed and processed;
        link_tags - list, a built-in list of the ready HTML tags which could
        contain the URLs in their attributes;
        kink_attrs - list, the list of ready HTML tag attributes which could
        contain the URLs inside.
        targ_file, str, the file which is created to write the result: all the
        URLs found on a particular webpage.
        """
        super().__init__()
        self.url = url
        self.link_tags = ['a', 'applet', 'base', 'bgsound', 'blockquote',
                          'body', 'button', 'command', 'del', 'div', 'embed',
                          'form', 'frame', 'head', 'html', 'iframe', 'img',
                          'input', 'ins', 'isindex', 'link', 'meta', 'object',
                          'q', 'source', 'svg', 'table', 'td', 'th', 'video']
        self.link_attrs = ['archive', 'codebase', 'href', 'src', 'cite',
                           'background', 'content', 'formaction', 'icon',
                           'pluginspage', 'action', 'profile', 'manifest',
                           'xmlns', 'lowsrc', 'classid', 'data', 'itemtype']
        self.targ_file = 'urls.txt'

    def clear_file(self):
        """
        the method which clears (truncates) the result file for writing new
        data in it
        """
        f = open(self.targ_file, 'w', encoding='utf-8')
        f.close()

    def get_urls(self):
        """
        the method which accepts a URL and gets the contents of that URL and
        feeds it to the built-in method of HTMLParser
        """
        r = requests.get(self.url)
        if r.status_code >= 200 and r.status_code < 400:
            r.encoding = 'utf-8'
            self.feed(r.text)
            return
        print('the request to the webpage failed')


    def write_to_file(self, link):
        """
        the method which writes ready URLs received after processing the input
        URL to a file
        params:
        link, str, the url which was found on a processed webpage
        """
        with open(self.targ_file, 'a', encoding='utf-8') as f:
            f.write(link + ' : 1\n')

    def write_count(self, url):
        """
        this method accepts a URL which has already been written to the result
        file and increases its count;
        params:
        url - str, the url which has already been found in a result file
        """
        with open(self.targ_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            cursor = content.find(url + ' : ') + len(url)
            f.seek(cursor)
            count = f.read(4).lstrip(' :')
            f.seek(cursor)
            #  if there are occurrences already - increase the number
            if count:
                count = int(count) + 1
                f.write(' : ' + str(count) + '\n')
                return
            f.write(' : 2\n')

    def check_url(self, url):
        """
        the method which checks the presence of a found URL in the result file:
        params:
        url - str, the URL which was found on a webpage
        return:
        True - if the URL is already in the result file
        False - if otherwise.
        """
        with open(self.targ_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if url in content:
                #  if it's there the full match should be checked:
                #  if the string is full - it should end with ' : <count>'
                #  if it does not - it matches only partially
                supposed_url = url + ' : '
                if supposed_url in content:
                    return True
            return False

    def handle_starttag(self, tag, attrs):
        """
        the overridden method of HTMLParser which handles HTML start tags
        params:
        tag - str, the name of the tag converted to lower case;
        attrs  - list, list of (name, value) pairs containing the attributes
        found inside the tag’s <> brackets.
        """
        if tag in self.link_tags:
            for attr in attrs:
                if attr[0] in self.link_attrs and attr[1].startswith('http'):
                    if not self.check_url(attr[1]):
                        self.write_to_file(attr[1])
                        return
                    self.write_count(attr[1])

    def handle_decl(self, decl):
        """
        the overridden method of HTMLParser which handles HTML doctype
        declaration
        params:
        decl - str, the entire contents of the declaration inside the <!...> 
        markup
        """
        # some links could appear in DOCTYPE declaration too
        if 'http' in decl:
            if not self.check_url(decl[decl.find('http'):len(decl)-1]):
                self.write_to_file(decl[decl.find('http'):len(decl)-1])
                return
            self.write_count(decl[decl.find('http'):len(decl)-1])


    def handle_comment(self, data):
        """
        the method which handles the HTML comments and looks for the URLs 
        inside them
        params:
        data - str, the contents of a comment inside <!-- -->
        """
        while 'http' in data:
            pattern = r"https?://[^\s,\'\"\)\(\}\{]+\.+[^\s,\'\"\)\(\}\{]+"
            match = re.search(pattern, data).group()
            if not self.check_url(match):
                self.write_to_file(match)
                data = data.replace(match, '', 1)
            else:
                self.write_count(match)
                data = data.replace(match, '', 1)


    def handle_data(self, data):
        """
        the overridden method of HTMLParser which handles arbitrary data
        between start and end tags
        params:
        data, str, the content located between start and end tags
        """
        while 'http' in data:
            pattern = r"https?://[^\s,\'\"\)\(\}\{]+\.+[^\s,\'\"\)\(\}\{]+"
            match = re.search(pattern, data)
            if match:
                if not self.check_url(match.group()):
                    self.write_to_file(match.group())
                    data = data.replace(match.group(), '', 1)
                else:
                    self.write_count(match.group())
                    data = data.replace(match.group(), '', 1)
            else:
                data = data.replace('http', '', 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', help='the url of the webpage you would like to\
            get urls from')
    args = parser.parse_args()
    if args.url:
        h = Page_Handler(args.url)
        h.clear_file()
        h.get_urls()
    else:
        print('you did not provide any URL to look for')

if __name__ == '__main__':
    main()
