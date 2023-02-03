from urllib.request import urlopen
from get_links import GetLinks
from shared import *


# create multiple spiders so that they can share the queue and visited_links resource
class Spider:
    # creating class variables to share among all instances/spiders
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()  # waiting list
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)  # providing an initial url as a starting point

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_files(Spider.project_name, Spider.base_url)
        Spider.queue = convert_file_to_set(Spider.queue_file)
        Spider.crawled = convert_file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' currently crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)               # moving the link from waiting list to visited
            Spider.crawled.add(page_url)
            Spider.update_files()

    # this function will connect to a website,
    # convert the html to a string html format,
    # pass that string to GetLinks,
    # GetLinks will parse the string and return all urls/links on the page
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':           # ensuring that the input is an html page
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")                    # converting the data to a string
            finder = GetLinks(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error : can not crawl the page')
            return set()                                                    # return an empty set if the try block fails
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:                               # if the target domain name is not in the url then continue to next
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        convert_set_to_file(Spider.queue, Spider.queue_file)
        convert_set_to_file(Spider.crawled, Spider.crawled_file)

