from abc import abstractmethod
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import urllib.robotparser
import re
import time

load_dotenv()

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:
    def __init__(self, url, pages_limit):
        self.visited_urls = []
        self.urls_to_visit = [url]
        self.logger = logging.getLogger('crawler_logger')
        self.pages_counter = 0
        self.pages_limit = pages_limit
        self.base_url = self.get_base_url(url)
        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(f"{self.base_url}/robots.txt")
        self.rp.read()

    def download_url(self, url):
        return requests.get(url, headers = {"HTTP_ACCEPT": "text/html"}).text

    def get_base_url(self, url):
        try:
            return re.search('https?:\/\/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url).group(0)
        except Exception:
            self.logger.exception(f'Failed to get base url from: {url}')
            return None

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path:
                if path.startswith('/'):
                    path = urljoin(url, path)
                    if self.can_visit_url(path):
                        yield path
                elif self.get_base_url(path) == self.base_url:
                    if self.can_visit_url(path):
                        yield path

    def can_visit_url(self, url):
        return self.rp.can_fetch("*", url)

    def delay_crawling(self):
        if self.rp.crawl_delay("*"):
            time.sleep(self.rp.crawl_delay("*"))
        else:
            time.sleep(25)

    @abstractmethod
    def add_url_to_visit(self, url):
        pass
    
    @abstractmethod
    def get_url_to_visit(self):
        pass

    def crawl(self, url):
        self.delay_crawling()
        html = self.download_url(url)
        self.pages_counter += 1
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit and self.pages_counter < self.pages_limit:
            url = self.get_url_to_visit()
            self.logger.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                self.logger.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

class BFSCrawler(Crawler):
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)
    
    def get_url_to_visit(self):
        return self.urls_to_visit.pop(0)

class HeuristicCrawler(Crawler):
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)
    
    def get_url_to_visit(self):
        return self.urls_to_visit.pop(0)

class CrawlerFactory():
    def __init__(self) -> None:
        pass
    
    def make_crawler(self, url, pages_limit=1000, default_strategy='bfs'):
        crawler_type = os.environ.get('CRAWLER_SELECTION_STRATEGY', default_strategy)
        if crawler_type.lower() == 'bfs': return BFSCrawler(url, pages_limit)
        elif crawler_type.lower() == 'heuristic': return HeuristicCrawler(url, pages_limit)
        else: logging.getLogger('crawler_logger').error(f'Invalid crawler selection strategy: {crawler_type}')

if __name__ == '__main__':
    CrawlerFactory().make_crawler(url='https://leitura.com.br/').run()