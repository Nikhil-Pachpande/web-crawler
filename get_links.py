from html.parser import HTMLParser
from urllib import parse


class GetLinks(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        # find the anchor tag
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)  # handling the relative url if it exists
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
