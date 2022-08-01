from abc import abstractmethod
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import urllib.robotparser
import re

load_dotenv()

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.logger = logging.getLogger('crawler_logger')

    def download_url(self, url):
        return requests.get(url).text

    def get_base_url(self, url):
        return re.search('https?:\/\/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url).group(0)

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path:
                if path.startswith('/'):
                    path = urljoin(url, path)
                    if self.can_visit_url(path):
                        yield path
                elif self.get_base_url(path) == self.get_base_url(url):
                    if self.can_visit_url(path):
                        yield path

    def can_visit_url(self, url):
        base_url = self.get_base_url(url)
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{base_url}/robots.txt")
        rp.read()
        print(url)
        return rp.can_fetch("*", url)

    @abstractmethod
    def add_url_to_visit(self, url):
        pass
    
    @abstractmethod
    def get_url_to_visit(self):
        pass

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
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
    
    def make_crawler(self, urls, default_strategy='bfs'):
        crawler_type = os.environ.get('CRAWLER_SELECTION_STRATEGY', default_strategy)
        if crawler_type.lower() == 'bfs': return BFSCrawler(urls)
        elif crawler_type.lower() == 'heuristic': return HeuristicCrawler(urls)
        else: logging.getLogger('crawler_logger').error(f'Invalid crawler selection strategy: {crawler_type}')

if __name__ == '__main__':
    CrawlerFactory().make_crawler(urls=['https://leitura.com.br/']).run()