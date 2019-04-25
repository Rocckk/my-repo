import scrapy
from scrapy.linkextractors import LinkExtractor
import re

class UrlSpider(scrapy.Spider):
    name = 'x_spider'

    def __init__(self, url=None):
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
        self.pattern = r"https?://[^\s,\'\"\)\(\}\{\<]+\.+[^\s,\'\"\)\(\}\{\<]+"
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
        match = re.search(self.pattern, value)
        if match:
            return match.group()

    def parse(self, response):
        list_of_links = [i.url for i in self.extractor.extract_links(response)]
        text_ls = [i.text for i in self.extractor.extract_links(response) if
                   'http' in i.text]
        for i in text_ls:
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

        #rint('##', list_of_links, len(list_of_links))
        no_duplicate_list = filter(lambda el: list_of_links.count(el) == 1,
                list_of_links)
        for i in no_duplicate_list:
            yield {'url' : i, 'count': list_of_links.count(i)}




