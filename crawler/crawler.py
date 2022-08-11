from abc import abstractmethod
import logging
from random import randrange
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import tldextract
import datetime
from robotparser import CustomRobotParser
import json

load_dotenv()

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:
    def __init__(self, url, pages_limit):
        self.visited_urls = []
        self.logger = logging.getLogger('crawler_logger')
        self.pages_counter = 0
        self.pages_limit = pages_limit
        self.domain = self.get_url_domain(url)
        with open('domain_config.json') as c:
            self.domain_config = json.load(c)
        try:
            delay_range = self.domain_config[self.domain]['crawl_delay_range']
            self.default_delay = lambda: randrange(delay_range[0], delay_range[1])
        except:
            self.default_delay = lambda: randrange(2, 6)
        self.driver = self.init_webdriver()
        self.rp = CustomRobotParser()
        self.rp.set_url(f"https://{self.get_url_netloc(url)}/robots.txt")
        self.rp.read_file(self.driver)
        self.urls_to_visit = []
        if self.can_visit_url(url):
            self.urls_to_visit.append(url)
    
    
    def init_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--log-level=1')
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def download_url(self, url):
        self.logger.info(f"Fetching html")
        self.driver.get(url)
        html = self.driver.page_source
        return html
    
    def save_page_source(self, html, url):
        file_dir = os.path.join('..', 'data', 'crawled', self.domain)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_name = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
        file_path = os.path.join(file_dir, f"{file_name}.html")
        self.logger.info(f"Saving page source to: {file_path}")
        file_metadata_path = os.path.join(file_dir, f"index.txt")
        try:
            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(html)
            f.close
            with open(file_metadata_path, "a", encoding="utf-8") as f:
                f.write(f"{file_name}: {url}\n")
            f.close
            self.pages_counter += 1
        except Exception:
            self.logger.exception(f"Failed to save page source")

    def get_url_netloc(self, url):
        try:
            return urlparse(url).netloc
        except Exception:
            self.logger.exception(f'Failed to get url netloc from: {url}')
            return None

    def get_url_domain(self, url):
        try:
            url_netloc = self.get_url_netloc(url)
            return tldextract.extract(url_netloc).domain
        except Exception:
            self.logger.exception(f'Failed to get url domain from: {url}')
            return None

    def get_linked_urls(self, url, html):
        self.logger.info(f"Getting linked urls")
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path:
                if path.startswith('/'):
                    path = urljoin(url, path)
                    if self.can_visit_url(path):
                        yield path
                elif self.get_url_domain(path) == self.domain:
                    if self.can_visit_url(path):
                        yield path

    def can_visit_url(self, url):
        return self.rp.can_fetch("*", url)

    def delay_crawling(self):
        if self.rp.crawl_delay("*"):
            time.sleep(self.rp.crawl_delay("*"))
        else:
            time.sleep(self.default_delay())

    @abstractmethod
    def add_url_to_visit(self, url):
        pass
    
    @abstractmethod
    def get_url_to_visit(self):
        pass

    def crawl(self, url):
        html = self.download_url(url)
        self.save_page_source(html, url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
        self.delay_crawling()

    def run(self):
        while self.urls_to_visit and self.pages_counter < self.pages_limit:
            url = self.get_url_to_visit()
            self.visited_urls.append(url)
            self.logger.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                self.logger.exception(f'Failed to crawl: {url}')

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