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

        # Request URL contents.
        url = self.base_url + '/econlog-author'
        response = self.make_request(url=url)   

        # Parse response as HTML
        html = self.content_parser(response=response)

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
        response = self.make_request(url=url)

        # Parse response as HTML.
        html = self.content_parser(response=response)

        # Find all article containers.
        containers = html.find_all('div', {'class': 'min-card-content'})

        return containers
    
    def extract_article_metadata(self, container_list):
        metadata = []
    
        for article in container_list:
            metadatum = {}

            metadatum['author'] = article.find('h3', {'class': 'ecolog-min-card-author'}).text.strip()
            metadatum['title'] = article.find('h5', {'class': 'min-card-title'}).text
            metadatum['url'] = article.find('h5', {'class': 'min-card-title'}).a['href']
            metadatum['date'] = (
                datetime.strptime(article.find('span', {'class': 'min-card-date'}).text, '%b %d %Y').strftime("%m-%d-%Y")
            )

            metadata.append(metadatum)

        return metadata
    
    def request_article_content(self, url):
        """
        For each article, request the content, returning the paragraph tags.
        
        Returns tuple with HTML.
        """

        # Request article content.
        response = self.make_request(url=url)

        # Parse article content as HTML.
        html = self.content_parser(response=response)

        # Post content is a list of paragraphs <p> tags.
        article_content = html.find('div', attrs={"class": "post-content"}).find_all('p')

        try:
            article_label = html.find('div', attrs={"class": "article-label"}).text.strip()
        except:
            article_label = ''

        return article_content, article_label