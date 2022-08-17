from crawler import CrawlerFactory

if __name__ == '__main__':
    CrawlerFactory().make_crawler(url='https://leitura.com.br/', pages_limit=10, default_strategy="heuristic").run()