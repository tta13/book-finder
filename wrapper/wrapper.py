from abc import abstractmethod
from pydoc import describe
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
        self.path = f'{base_path}/{self.domain}'

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

class CulturaWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'livrariacultura'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        def treat_author(author_string: str):
            authors = author_string.split('|')
            result = []
            for a in authors:
                if not 'Autor' in a:
                    continue
                name = a.replace('Autor:', '')
                name = name.split(', ')
                name.reverse()
                result.append(' '.join(name))
            return result
        
        title_div = soup.find("h1", class_="title_product").div
        if title_div:
            title = title_div.string
        publisher_div = soup.find('div', class_='publisher')
        publisher = publisher_div.h2.div.a.string if publisher_div.h2.div else ''
        info_div = soup.find('div', id='info-product')
        book_info = info_div.string.strip('\n ') if info_div else ''
        price_data = soup.find('em', class_='valor-por')
        price = price_data.strong.text if price_data else ''
        prod_spec = soup.find(class_='section-produto-especificacoes')
        if not publisher:
            publisher_data = prod_spec.find('td', class_='value-field Editora')
            publisher = publisher_data.string if publisher_data else ''
        author_data = prod_spec.find('td', class_='value-field Colaborador')
        authors = treat_author(author_data.string) if author_data else []
        isbn_data = prod_spec.find('td', class_='value-field ISBN')
        isbn = isbn_data.string if isbn_data else ''  
        language_data = prod_spec.find('td', class_='value-field Idioma')
        language = language_data.string if isbn_data else ''
        year_data = prod_spec.find('td', class_='value-field Ano')
        year = year_data.string if year_data else ''
        edition_data = prod_spec.find('td', class_='value-field Edicao')
        edition = edition_data.string if edition_data else ''
        pages_data = prod_spec.find('td', class_='value-field Paginas')
        pages = pages_data.string if pages_data else ''
        return {
            "title": title,
            "publisher": publisher,
            "price": price,
            "info": book_info,
            "authors": authors,
            "year": year,
            "isbn": isbn,
            "edition": edition,
            "pages": pages,
            "language": language
        }

class CompanhiaWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'companhiadasletras'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_div = soup.find('div', class_='detalhe_livro_titulo')
        title = title_div.string if title_div else ''
        authors_div = soup.find('div', class_='detalhe_livro_autor')
        authors=[]
        if authors_div:
            for a in authors_div.find_all('a'):
                authors.append(a.string)
        price_div = soup.find('div', class_='preco')
        price = price_div.string if price_div else ''
        details = soup.find_all('div', class_='bloco_txt_detalhe')
        book_info = details[0].get_text().strip('\n ') if details else ''
        pages, year, isbn, publisher = '', '', '', ''
        for span in details[1].find_all('span'):
            if span.string == 'Páginas:':
                pages = str(span.next_sibling).strip()
            if span.string == 'Lançamento:':
                year = str(span.next_sibling).split('/')[-1]
            if span.string == 'ISBN:':
                isbn = str(span.next_sibling).strip()
            if span.string == 'Selo:':
                publisher = str(span.next_sibling).strip()
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": book_info,
            "year": year,
            "isbn": isbn,
            "edition": '',
            "pages": pages,
            "language": ''
        }

class EstanteWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'estantevirtual'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_h1 = soup.find('h1', class_='livro-titulo')
        title = title_h1.string.strip('\n ') if title_h1 else ''
        authors_h2 = soup.find('h2', class_='livro-autor')
        authors = authors_h2.a.span.string.split('; ') if authors_h2 else ''
        price_span = soup.find('span', class_='livro-preco-valor')
        price = price_span.string.strip('\n ') if price_span else ''
        specs = soup.find_all('p', class_='livro-specs')
        year, publisher, isbn, language, book_info = '', '', '', '', ''
        for spec in specs:
            if 'Ano' in str(spec.span.string):
                year = spec.span.next_sibling.strip('\n ')
            elif 'Editora' in str(spec.span.string):
                publisher = spec.a.span.string
            elif 'ISBN' in str(spec.span.string):
                isbn = spec.span.next_sibling.strip('\n ')
            elif 'Idioma' in str(spec.span.string):
                language = spec.span.next_sibling.strip('\n ')
            elif 'Descrição' in str(spec.span.string):
                book_info = spec.find('span', class_='description-text').string.strip('\n ')
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": book_info,
            "year": year,
            "isbn": isbn,
            "edition": '',
            "pages": '',
            "language": language
        }

class SaraivaWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'saraiva'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_element = soup.find('h1', class_='title')
        title = title_element.string.strip() if title_element else ''
        price_p = soup.find('p', class_='price-destaque')
        price = price_p.string.strip() if price_p else ''
        info_div = soup.find('div', id='descricao')
        info = info_div.text.strip('\n ') if info_div else ''
        features = soup.find('div', id='caracteristicas').div.div.div.table.tbody
        year, authors, isbn, edition, language, pages, publisher = '', [], '', '', '', '', ''
        if features:
            for tr in features.find_all('tr'):
                tds = tr.find_all('td')
                field, data = tds[0], tds[1]
                if not field or not data:
                    continue
                field, data = field.string.lower(), data.string
                if 'ano da edição' in field:
                    year = data.strip()
                elif 'isbn' in field:
                    isbn = data.strip()
                elif 'idioma' in field:
                    language = data.strip()
                elif 'número da edição' in field:
                    edition = data.strip()
                elif 'páginas' in field:
                    pages = data.strip()
                elif 'marca' in field:
                    publisher = data.strip()
                elif 'autor' in field:
                    name_list = data.split(',')
                    names, first_names = name_list[::2], name_list[1::2]
                    first_names.extend(['' for i in range(len(names)-len(first_names))])
                    authors = [' '.join([y, x]).strip() for x, y in zip(names, first_names)]
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": info,
            "year": year,
            "isbn": isbn,
            "edition": edition,
            "pages": pages,
            "language": language
        }

class LeituraWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'leitura'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_header = soup.find('h1', class_='product-title')
        title = title_header.string.strip('\n ') if title_header else ''
        price_p = soup.find('p', class_='price')
        price = price_p.string.strip('\n\t ') if price_p else ''
        description = soup.find('div', id='tab-description')
        info_p = description.p if description else None
        info = info_p.text.strip('\n\t ') if info_p else ''
        details = soup.find('div', id='tab-details')
        isbn = ''
        if details.table:
            for tr in details.table.tbody.find_all('tr'):
                field, content = tr.td, tr.td.next_sibling.next_sibling
                if field and content:
                    if 'código de barras' in str(field.string).lower():
                        isbn = content.string.strip()
        details = soup.find('div', id='tab-specification').table
        authors, publisher, language, pages, year = [], '', '', '', ''
        if details:
            for tr in details.tbody.find_all('tr'):
                field, content = tr.td, tr.td.next_sibling.next_sibling
                if field and content:
                    field, content = field.string.lower(), content.string
                    if 'autor' in field:
                        authors = content.split(' & ')
                    elif 'editora' in field:
                        publisher = content.strip()
                    elif 'idioma' in field:
                        language = content.strip()
                    elif 'páginas' in field:
                        pages = content.strip()
                    elif 'ano de' in field:
                        year = content.strip()
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": info,
            "year": year,
            "isbn": isbn,
            "edition": '',
            "pages": pages,
            "language": language
        }

class TravessaWrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'travessa'
        self.path = f'{base_path}/{self.domain}'

    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_span = soup.find('span', id='lblNomArtigo')
        title = title_span.string.strip() if title_span else ''
        publisher_span = soup.find('span', id='lblNomProdutor')
        publisher = publisher_span.a.string.strip() if publisher_span and publisher_span.a else ''
        price_el = soup.find('strong', id='litPreco')
        price = price_el.string.strip() if price_el else ''
        info_el = soup.find('p', id='lblSinopse')
        info = info_el.text.strip('\n ') if info_el else ''
        data = soup.find('div', class_='dados')
        isbn, language, pages, year, edition, authors = '', '', '', '', '', []
        if data:
            title_data = data.find('span', id='lblDadosNome')
            title = title_data.text.strip('\n ') if title_data else title
            isbn_data = data.find('span', id='lblDadosIsbn')
            isbn = isbn_data.text.strip('\n ') if isbn_data else ''
            language_data = data.find('span', id='lblDadosIdioma')
            language = language_data.text.strip('\n ') if language_data else ''
            pages_data = data.find('span', id='lblDadosPaginas')
            pages = pages_data.text.strip('\n ') if pages_data else ''
            y_data = data.find('span', id='lblDadosAnoEdicao')
            year = y_data.text.strip('\n ') if y_data else ''
            ed_data = data.find('span', id='lblDadosEdicao')
            edition = ed_data.text.strip('\n ') if ed_data else ''
            authors_data = data.find('span', id='lblTituloDadosParticipantes')
            if authors_data:
                for c in authors_data.children:
                    if c.name == 'br':
                        break
                    elif c.name == 'a':
                        authors.append(c.string.strip())
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": info,
            "year": year,
            "isbn": isbn,
            "edition": edition,
            "pages": pages,
            "language": language
        }

class Book7Wrapper(Wrapper):
    def __init__(self, base_path):
        super().__init__(base_path)
        self.domain = 'book7'
        self.path = f'{base_path}/{self.domain}'
    
    def extract_info(self, soup: BeautifulSoup) -> dict:
        title_h = soup.find('h1', class_='product__name')
        title = title_h.string.strip('\n ') if title_h else ''
        description = soup.find('div', class_='info')
        info = ''
        if description:
            for child in description.children:
                if child.name == 'p':
                    info = child.text.strip('\n ')
        publisher_and_author = soup.find('div', class_='product__descriptions')
        authors, publisher = [], ''
        if publisher_and_author:
            for c in publisher_and_author.children:
                if not c.name == 'p': continue
                split_content = c.text.strip(' ').split(':')
                name, content = split_content[0], split_content[1]
                if 'autor' in name.lower():
                    authors = [('').join(reversed(x.split(','))).strip() for x in content.split(';')]
                if 'marca' in name.lower():
                    publisher = content.strip('\n ')
        price_h = soup.find('h4', id='price__best')
        price = price_h.text.strip('\n ') if price_h else ''
        content_specification = soup.find('div', class_='content__specification')
        content_table = content_specification.table if content_specification else None
        isbn, year, edition, pages = '', '', '', ''
        if content_table:
            for tr in content_table.find_all('tr'):
                name, content = tr.th, tr.td
                if not name or not content: continue
                if 'ean' in name.string.lower():
                    isbn = content.text.strip('\n ')
                elif 'ano da edição' in name.string.lower():
                    year = content.text.strip('\n ')
                elif 'edição' in name.string.lower():
                    edition = content.text.strip('\n ')
                elif 'páginas' in name.string.lower():
                    pages = content.text.strip('\n ')
        return {
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "price": price,
            "info": info,
            "year": year,
            "isbn": isbn,
            "edition": edition,
            "pages": pages,
            "language": ''
        }
