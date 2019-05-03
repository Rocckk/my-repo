"""
this module implements a spider, which crawls a webpage passed to it as an
argument and scrapes all the links it has in its tags and it text nodes.
Example:
scrapy crawl x_spider -a url=https://someurl.to_scrapte.com/
"""

import re
import scrapy
from scrapy.linkextractors import LinkExtractor


class UrlSpider(scrapy.Spider):
    """
    this class is a spider itself which extends the abilities of built-in
    scrapy.Spider class; 
    it defines how a certain webpage will be scraped: form which tags and
    attributes the links will be extracted and also enables extraction of links
    from texrt import nodes
    """
    name = 'x_spider'

    def __init__(self, url=None):
        """
        the initializer of class' instances which sets necessary instance
        variables and enable the spider to access them during execution
        params:
        url - str, the url of the webpage which will be parsed

        instance attributes:
        self.start_urls  - see above
        self.link_tags - tuple, the tags from which the links will be extracted
        self.link_attrs - tuple, the tag attributes from which the links will be
        extracted
        self.pattern - the regex which will be used to extract links from text
        nodes
        self.tag_attr_combos - tuple,the combinations of a tag and attribute
        which will be looked for to extract links; useful because some tags have
        common  attributes, an some of this attributes can contain links in one
        tags,but they are not a place for links in other tags
        self.extractor - thr instance of a built-in LinkExtracto which will be
        used for extraction of links from a webpage
        """
        super().__init__()
        self.start_urls = [url]
        self.link_tags = ('a', 'applet', 'base', 'bgsound', 'blockquote',
                          'body', 'button', 'command', 'del', 'div', 'embed',
                          'form', 'frame', 'head', 'html', 'iframe', 'img',
                          'input', 'ins', 'isindex', 'link', 'meta', 'object',
                          'q', 'source', 'svg', 'table', 'td', 'th', 'video')
        self.link_attrs = ('archive', 'codebase', 'href', 'src', 'cite',
                           'background', 'content', 'formaction', 'icon',
                           'pluginspage', 'action', 'profile', 'manifest',
                           'xmlns', 'lowsrc', 'classid', 'data', 'itemtype')
        self.pattern = \
            r"https?://[^\s,\'\"\)\(\}\{\<\\]+\.+[^\s,\'\"\)\(\}\{\<\\]+"
        self.tag_attr_combos = ('a[href]', 'applet[archive]', 'applet[codebase]',
                                'base[href]', 'bgsound[src]', 'blockquote[cite]',
                                'body[background]', 'button[formaction]',
                                'command[icon]', 'del[cite]', 'div[itemtype]',
                                'embed[src]', 'form[action]', 'frame[src]',
                                'head[profile]', 'html[manifest]', 'html[xmlns]',
                                'iframe[src]', 'img[src]', 'input[formaction]',
                                'input[src]', 'ins[cite]', 'isindex[action]',
                                'link[href]', 'meta[itemtype]',
                                'object[archive]', 'object[codebase]', 'q[cite]',
                                'source[src]', 'svg[itemtype]',
                                'table[background]', 'td[background]',
                                'th[background]', 'video[src]',
                                'embed[pluginspage]', 'img[lowsrc]',
                                'object[classid]', 'object[data]')
        self.extractor = LinkExtractor(process_value=self.regex_link,
                                       tags=self.link_tags,
                                       attrs=self.link_attrs, unique=False,
                                       restrict_css=self.tag_attr_combos)

    def regex_link(self, value):
        """
        this function ensures that the value received from a scanned tag or
        attribute will match self.pattern
        params:
        value - str, the value of a tag/attribute which is scanned by a link
        extractor
        returns:
        the same value if it matches the pattern
        """
        match = re.search(self.pattern, value)
        if match:
            return match.group()

    def parse(self, response):
        """
        this method is  a modified method is in charge of processing the 
        response and returning scraped data: it accepts a Response object
        received from the scraped webpage, extracts the links from it and
        creates a list of those links; later on, this list is looped through
        and, a dict is created from its items and yielded to the Pipeline
        params:
        response - the Response object to parse
        returns:
        a dict containing the url
        """
        extracted_links = self.extractor.extract_links(response)
        list_of_links = [i.url for i in extracted_links]
        text_links = [i.text for i in extracted_links if 'http' in i.text]
        for i in text_links:
            while 'http' in i:
                match = re.search(self.pattern, i)
                if match:
                    if match.group() not in list_of_links:
                        list_of_links.append(match.group())
                        i = i.replace(match.group(), '', 1)
                    else:
                        i = i.replace(match.group(), '', 1)
                else:
                    i = i.replace('http', '', 1)
        for i in list_of_links:
            yield {'url': i}
