from crawler import CrawlerFactory

if __name__ == '__main__':
    CrawlerFactory().make_crawler(urls=['https://leitura.com.br/']).run()