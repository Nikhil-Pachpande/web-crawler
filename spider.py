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
            Spider.add_links_to_queue(Spider.gather_link(page_url))
            Spider.queue.remove(page_url)               # moving the link from waiting list to visited
            Spider.crawled.add(page_url)
            Spider.update_files()