import datetime
import os

import lxml.html
import requests
from picklecache import cache

@cache(os.path.join('~', '.muckrock'))
def get(url):
    headers = {'User-Agent': 'https://pypi.python.org/pypi/muckrock'}
    return requests.get(url, headers = headers)

def listings():
    url = 'https://www.muckrock.com/foi/list/?page=1'
    while True:
        response = get(url)
        html = lxml.html.fromstring(response.text)
        html.make_links_absolute(response.url)
        downloaded_time = datetime.datetime.strptime(response.headers['Date'],
                                                     '%a, %d %b %Y %H:%M:%S GMT')
        yield from parse_listings(html, downloaded_time)
        maybe_next_page = html.xpath('//a[text()="Next page »"]/@href')
        if len(maybe_next_page) == 0:
            break
        else:
            url = maybe_next_page[0]

def parse_listings(html, downloaded_time):
    for tr in html.xpath('//table[@class="data-table"]/tr')[1:]:
        quiet = tr.xpath('td[position()=1]/em/text()')
        tags = [] if quiet == [] else quiet[0].split(', ')
        yield {
            'downloaded': downloaded_time,
            'request': str(tr.xpath('td[position()=1]/a/@href')[0]),
            'title': str(tr.xpath('td[position()=1]/a/text()')[0]),
            'tags': list(map(str, tags)),
            'user': str(tr.xpath('td[position()=2]/a/@href')[0]),
            'status': str(tr.xpath('td[position()=3]/span/text()')[0]),
            'jurisdiction': str(tr.xpath('td[position()=4]/a/@href')[0]),
            'date': datetime.datetime.strptime(tr.xpath('td[position()=5]/text()')[0].strip(), '%b. %d, %Y').date(),
        }

def main():
    for listing in listings():
        pass
