"""
This module implements a Github web crawler, which accepts a standardized json input which is read
from a json file that is piped to the script as the standard input (stdin), e.g:
>>python github_crawler.py < input.json

The input file should contain 3 keys: keywords, proxies, type.
The value of 'keywords' key should be an array of 3 keywords to search for on Github:
"keywords": ["python", "vagrant", "django"]

The value of 'proxies' key should be an array of 2 proxy server's URLs with their schemas
included:
"proxies": ["80.255.91.38:43360", "118.97.235.234:8080"]

The value of 'type' key should be an string with one of the following 3 values: 'Repositories',
'Issues', 'Wikis', which indicates search sections of Github to search through:
"type": "Issues"

The crawler searches for the keywords on Github and returns a json file with the result (URLs which
match search criteria). For types 'Issues' and 'Wikis' the result will have the following schema:
[
    {
        "url": "https://github.com/andreagrandi/covid-api/issues/1"
    },
    {
        "url": "https://github.com/Prefeitura-Comunica/thread/issues/3"
    }
]
For Repositories, it will additionally include information on a repo owner and languages used for
the repo. The schema is as follows:
[
    {
        "url": "https://github.com/davidfischer-ch/ansible-roles",
        "extra": {
            "owner": "davidfischer-ch",
            "language_stats": {
                "Python": 99.9,
                "Shell": 0.1
            }
        }
    }
]
"""
import concurrent.futures
import json
import sys

from lxml.html import fromstring

import requests

OBJECT_TYPES = ['Repositories', 'Issues', 'Wikis']


def get_input(content):
    """
    This function accepts a file-like object (stdin) with json input and extracts necessary data
    from it
    :param content: file-like object with input
    :return: tuple containing proxies to use for requests, keywords to search for and type of
    Github section to search for.
    """
    obj = json.loads(content)
    keywords = obj.get('keywords')
    obj_type = obj.get('type')
    return keywords, obj_type


def parse_repo(url):
    """
    This function sends requests to repo URL, parses it and extracts necessary data
    :param url: string, the URL of Github repo
    :param proxies: dict, dict where key is the schema and value is the actual URL of a proxy
    {'https': 'https://81.33.4.214:61711', 'http': 'http://185.176.32.160:3128'}

    :return: dict, dict containing the URL of the page, the owner of the repo and repo's language
    statistics
    """
    r = requests.get(url)
    result_html = fromstring(r.text)
    langs = [
        i.get('aria-label') for i in result_html.cssselect(
            'div.d-flex.repository-lang-stats-graph span'
        )
    ]
    owner = result_html.cssselect('span.author.ml-1.flex-self-stretch[itemprop=author] a')[0]
    return {
        'url': url,
        'extra': {
            'owner': owner.text_content(), 'language_stats': {
                ' '.join(i.split()[:-1]): float(i.split()[-1].rstrip('%')) for i in langs
            }
        }
    }


def get_urls(keywords, obj_type):
    """
    This function retrieves URLs matching search keywords passsed as the input
    :param keywords: list, the list of keywords to search for
    :param proxies: list, list of dicts where key is the schema and value is the actual URL of a proxy
    {'https': 'https://81.33.4.214:61711', 'http': 'http://185.176.32.160:3128'}
    :param obj_type: string, the type of Github section to search through
    :return: list, list of dictionaries where key is always 'url' and value is the URL of the page
    which is suitable
    """
    if obj_type == OBJECT_TYPES[0]:
        github_url = 'https://github.com/search?utf8=%E2%9C%93&q=topic%3A{}+topic%3A{}+topic%3A{}&\
ref=simplesearch'.format(keywords[0], keywords[1], keywords[2])
    elif obj_type == OBJECT_TYPES[1]:
        github_url = 'https://github.com/search?q={}+{}+{}+type%3Aissue'.format(
            keywords[0], keywords[1], keywords[2]
        )
    elif obj_type == OBJECT_TYPES[2]:
        github_url = 'https://github.com/search?q={}+{}+{}&type=Wikis'.format(
            keywords[0], keywords[1], keywords[2]
        )
    r = requests.get(url=github_url)
    result_html = fromstring(r.text)
    urls = [
        {'url': 'https://github.com' + i.get('href')} for i in result_html.cssselect(
            'div.f4.text-normal a'
        )
    ]
    return urls


def get_extra(urls, obj_type):
    """
    This function concurrently sends requests to Github repo URLs passed as its parameter and
    returns the structured result containing the URL, owner and language stats for this URL
    :param urls: list, the array of dicts of URLs of Github repos
    :param obj_type: string, the type of Github section to search through
    :param proxies: list, list of dicts here key is the schema and value is the actual URL of a proxy
    {'https': 'https://81.33.4.214:61711', 'http': 'http://185.176.32.160:3128'}
    :return: list, the list of dicts containing the URL of the page, the owner of the repo and
    repo's language statistics
    """
    if obj_type == OBJECT_TYPES[0]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
            future_to_url = {
                executor.submit(parse_repo, url.get('url')): url.get('url') for url in urls
            }
            results = [future.result() for future in concurrent.futures.as_completed(future_to_url)]
            return results


def write_results(results):
    with open('result.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def main():
    content = sys.stdin.read()
    keywords, obj_type = get_input(content)
    urls = get_urls(keywords, obj_type)
    results = get_extra(urls, obj_type)
    if results:
        write_results(results)
    else:
        write_results(urls)


if __name__ == '__main__':
    main()
