import threading
from queue import Queue
from spider import Spider
from scan import Scan
from domain import *
from shared import *

PROJECT_NAME = 'toscrape'
HOMEPAGE = 'https://toscrape.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 16
queue = Queue()  # thread queue
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


def crawl():
    queued_links = convert_file_to_set(QUEUE_FILE)
    link_num = len(queued_links)
    if link_num > 0:
        print(str(link_num) + 'links remaining...')
        create_jobs(queued_links)


def scan():
    with open(Spider.project_name + '/crawled.txt', 'r') as crawled_urls:
        for url in crawled_urls:
            if Scan.is_url_insecure(url):
                insecure_urls = Scan.insecure_set
                convert_set_to_file(insecure_urls, Spider.project_name + '/insecure_urls.txt')
            url = url.strip()
            sqli_urls = Scan.is_url_vulnerable_to_sql_injection(url)
            xss_urls = Scan.is_url_vulnerable_to_xss(url)
            csrf_urls = Scan.is_url_vulnerable_to_csrf(url)
            ssrf_urls = Scan.is_url_vulnerable_to_ssrf(url)
            lfi_urls = Scan.is_url_vulnerable_to_lfi(url)
            rce_urls = Scan.is_url_vulnerable_to_rce(url)
            convert_set_to_file(sqli_urls, Spider.project_name + '/sql_injection_vulnerabilities.txt')
            convert_set_to_file(xss_urls, Spider.project_name + '/xss_vulnerabilities.txt')
            convert_set_to_file(csrf_urls, Spider.project_name + '/csrf_vulnerabilities.txt')
            convert_set_to_file(ssrf_urls, Spider.project_name + '/ssrf_vulnerabilities.txt')
            convert_set_to_file(lfi_urls, Spider.project_name + '/lfi_vulnerabilities.txt')
            convert_set_to_file(rce_urls, Spider.project_name + '/rce_vulnerabilities.txt')
        print("Scan Completed!")


def create_jobs(queued_links):
    for link in queued_links:
        queue.put(link)
    # prevent race conditions
    # tell thread to 'wait its turn'
    queue.join()
    crawl()


def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        # to ensure that it's a daemon process and dies with main
        t.daemon = True
        t.start()


# to assign work to the spiders
def work():
    while True:
        link = queue.get()
        Spider.crawl_page(threading.current_thread().name, link)
        queue.task_done()


create_spiders()
crawl()
scan()