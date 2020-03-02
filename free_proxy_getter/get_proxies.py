import requests
from lxml.html import fromstring


def get_proxies():
    r = requests.get('https://free-proxy-list.net/')

    page = fromstring(r.text)

    urls = [i.text_content() for i in page.cssselect('table#proxylisttable tbody tr td:first-child')]
    ports = [':' + i.text_content() for i in page.cssselect('table#proxylisttable tbody tr td:nth-child(2)')]
    schemas = list(map(
        lambda x: 'https://' if x == 'yes' else 'http://', [
            i.text_content() for i in page.cssselect('table#proxylisttable tbody tr td:nth-child(7)')
        ]
    ))

    proxy_list = [schemas[i[0]] + i[1] + ports[i[0]] for i in enumerate(urls)]
    print(proxy_list)
    return proxy_list


if __name__ == '__main__':
    get_proxies()
