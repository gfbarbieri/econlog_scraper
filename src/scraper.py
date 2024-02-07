from bs4 import BeautifulSoup
import requests
from datetime import datetime

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

    def make_request(self, url, params=None):
        """
        Performs GET requests. Returns HTML.
        """

        try:
            response = requests.get(url, headers=self.headers, params=params)
        except Exception as e:
            raise e
        
        return response

    def content_parser(self, response, parser='html.parser'):

        content = response.content
        soup = BeautifulSoup(markup=content, features=parser)

        return soup
    
    def request_parse(self, url):

        response = self.make_request(url=url)
        soup = self.content_parser(response=response)

        return soup

class EconlogScraper(Scraper):

    def __init__(self, base_url='https://www.econlib.org', author='bcaplan'):
        super().__init__(base_url=base_url)
        self.author = author

    def request_authors(self):
        """
        Extracts all of the authors from the EconLog website. Returns a dictionary with the authors name (First, Last)
        and their name tag in the websites HTML code.
        """
        author_list = {}

        # Request HTML contents.
        url = self.base_url + '/econlog-author'
        html = self.request_parse(url=url)

        # For each author, add the authors name (Last, First) and the author's user name.
        for author in html.find_all('div', {'class':'title-cell'}):
            last_first = author.find('a').text
            user = author.find('a').get('href').split('#')[1].replace(' ', '-').lower()
            
            author_list[last_first] = user

        return author_list

    def request_article_containers(self):
        """
        Download the HTML containers used to store the article's metadata.

        Returns a list where each item is an article's HTML container.
        """

        # Request URL contents.
        url = self.base_url + f"/author/{self.author}"
        html = self.request_parse(url=url)

        # Find all article containers.
        containers = html.find_all('div', {'class': 'min-card-content'})

        return containers
    
    def request_article_content(self, url):
        """
        For each article, request the content, returning the paragraph tags.
        
        Returns tuple with HTML.
        """

        # Request article content.
        html = self.request_parse(url=url)

        # Post content is a list of paragraphs <p> tags.
        article_content = html.find('div', attrs={"class": "post-content"}).find_all('p')

        try:
            article_label = html.find('div', attrs={"class": "article-label"}).text.strip()
        except:
            article_label = ''

        return article_content, article_label
    
    def extract_article_metadata(self, article_container):

        metadata = {}

        metadata['author'] = article_container.find('h3', {'class': 'ecolog-min-card-author'}).text.strip()
        metadata['title'] = article_container.find('h5', {'class': 'min-card-title'}).text
        metadata['url'] = article_container.find('h5', {'class': 'min-card-title'}).a['href']
        metadata['date'] = (
            datetime.strptime(article_container.find('span', {'class': 'min-card-date'}).text, '%b %d %Y').strftime("%m-%d-%Y")
        )

        return metadata
    
    def extract_article_text(self, article_content):
        """
        Extract the article's text from the 'p' tags.
        
        Return a document (string).
        """

        text = []

        for p_tag in article_content:
            text.append(p_tag.text)

        return " ".join(text)
    
    def extract_embedded_urls(self, article_content):
        """
        Extract the URLs embedded in article text, defined by 'p' tags. Returns a list of URLs.
        """

        embedded_urls = set()

        for p_tag in article_content:
            urls = p_tag.find_all('a')

            for url in urls:
                embedded_urls.add(url.get('href'))

        return embedded_urls