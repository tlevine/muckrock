import lxml.html
from picklecache import cache

@cache(os.path.join('~', '.muckrock'))
def get(url):
    return requests.get(url)

def listings():
    url = 'https://www.muckrock.com/foi/list/?page=1'
    while True:
        response = get(url)
        html = lxml.html.fromstring(response.text)
        html.make_links_absolute(response.url)
        yield from parse_listings(html)
        maybe_next_page = html.xpath('//a[text()="Next page »"]/@href')
        if len(maybe_next_page) == 0:
            break
        else:
            url = maybe_next_page[0]

def parse_listings(html):
    return []

def main():
    for listing in listings():
        pass
