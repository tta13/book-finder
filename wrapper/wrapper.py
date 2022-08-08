from abc import abstractmethod
from bs4 import BeautifulSoup
import os
import re
import json

class Wrapper:
    def __init__(self, base_path):
        self.path = base_path
        self.domain = ''
    
    def save_page_info(self, book, content):
        file_dir = os.path.join('..', 'data', 'wrapped', self.domain)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = os.path.join(file_dir, f"{book}.json")
        print(f"Saving page info to: {file_path}")
        try:
            with open(file_path, 'w', encoding='utf-8') as outfile:
                json.dump(content, outfile, ensure_ascii=False, indent=1)
        except Exception:
            print(f"Failed to save page info")

    def wrap(self):
        for book in os.listdir(self.path):
            file = os.path.join(self.path, book)
            if book.endswith('.html'):
                html = open(file, 'r', encoding='utf-8')
                self.save_page_info(book, self.extract_info(BeautifulSoup(html, 'html.parser')))
    
    @abstractmethod
    def extract_info(self, soup: BeautifulSoup) -> dict:
        pass

class AmazonWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'amazon'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title = soup.find('span', id='productTitle').string.strip('\n ')
        info = ''
        description_div = soup.find('div', id='bookDescription_feature_div')
        if description_div:
            info = description_div.div.div.text.strip('\n ')
        authors_spans = soup.find('div', id='bylineInfo').find_all('span', class_='author')
        authors = []
        if authors_spans:
            for author in authors_spans:
                if 'Autor' in str(author.find('span', class_='contribution').span.string):
                    if author.a:
                        result = str(author.a.string)
                        authors.append(result if 'Visite' not in result else result.replace('Visite a página de ', ''))
        price_span = soup.find('span', id='price')
        price = ''
        if price_span:
            price = str(price_span.string).replace(u'\xa0', u' ')
        details = soup.find('div', id='detailBulletsWrapper_feature_div')
        publisher, year, isbn, edition, pages, language = '', '', '', '', '', ''
        for li in details.div.ul.find_all('li'):
            field = str(li.span.span.string)
            content = str(li.span.find_all('span')[-1].string)
            if 'Editora' in field:  
                publication_info = content
                if ';' in publication_info:
                    split_publication_info = publication_info.split(';')
                    publisher = split_publication_info[0]
                    if 'edição' in split_publication_info[1]:
                        year_and_edition_info = split_publication_info[1].split(' edição ')
                        edition = year_and_edition_info[0].strip()
                        year = re.search(r'[0-9][0-9][0-9][0-9]', year_and_edition_info[1]).group(0)
                    else:
                        year = re.search(r'[0-9][0-9][0-9][0-9]', split_publication_info[1]).group(0)
                else:
                    publisher = str(li.span.find_all('span')[-1].string).strip()
            elif 'Idioma' in field:
                language = content
            elif 'página' in content:
                pages = re.search(r'[0-9]+', content).group(0)
            elif 'ISBN' in field:
                isbn = content
        return {
            "title": title,
            "publisher": publisher,
            "price": price,
            "info": info,
            "authors": authors,
            "year": year,
            "isbn": isbn,
            "edition": edition,
            "pages": pages,
            "language": language
        }
