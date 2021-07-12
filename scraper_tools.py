from bs4 import BeautifulSoup
from datetime import datetime
import requests

def make_request(url, params=None):
    """
    Performs GET requests. Returns HTML.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Request the HTML from EconLog and parse the content.
    response = requests.get(url, headers=headers, params=params)
    html = BeautifulSoup(response.content, 'html.parser')

    return html

def request_containers(author, year):
    """
    Download the HTML containers used to store the article's metadata for a given year.
    Returns a list where each item is an article's HTML container.
    """

    # Request the authors article's posted in the defined year.
    url = 'https://www.econlib.org/author/{}/'.format(author)
    html = make_request(url=url, params={'selected_year': year})

    # Compile a complete list of posts for the year.
    containers = html.find_all('div', {'class': 'min-card-posts-container'})

    return containers

def request_article(url):
    """
    For each article, request the content, returning the paragraph tags. Returns HTML.
    """
    html = make_request(url=url)

    # Post content is a list of paragraphs <p> tags.
    article_content = html.find('div', attrs={"class": "post-content"}).find_all('p')

    try:
        article_label = html.find('div', attrs={"class": "article-label"}).text.strip()
    except:
        article_label = ''

    return article_content, article_label

def extract_authors():
    """
    Extracts all of the authors from the EconLog website. Returns a dictionary with the authors name (First, Last)
    and their name tag in the websites HTML code.
    """
    author_list = dict()

    url = 'https://www.econlib.org/econlog-author'
    html = make_request(url=url)

    # For each author, add the authors name (Last, First) and the author's user name.
    for author in html.find_all('div', {'class':'title-cell'}):
        author_list[author.find('a').text] = author.find('a').get('href').split('#')[1]

    return author_list

def extract_years(author):
    """
    Extract all of the years an author published an article. Returns a list of the years formatted as integers.
    """
    years = []

    url = 'https://www.econlib.org/author/{}'.format(author)
    html = make_request(url=url)

    for year in html.find_all('div', {'class':"dropdown-menu dropdown-menu-right"})[0].find_all('a'):
        years.append(int(year.text))

    return years

def extract_metadata(container):
    """
    For each article container, extract the metadata. Each container has the articles URL, title and date posted.
    Returns a dictionary where each item is the articlces URL, title and date posted.

    pd.to_datetime(container.find('span', {'class':'min-card-date'}).text, format="%b %d %Y")
    """
    metadata = dict()

    # For each post, extract the metadata: title, date, and url.
    metadata['url'] = container.find('a').get('href')
    metadata['title'] = container.find('a').text
    metadata['date'] = datetime.strptime(container.find('span', {'class':'min-card-date'}).text, '%b %d %Y')

    return metadata

def extract_urls(article):
    """
    """
    embedded_urls = set()

    for p_tag in article:
        urls = p_tag.find_all('a')

        for url in urls:
            embedded_urls.add(url.get('href'))

    return embedded_urls
