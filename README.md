# Econlog Article Scaper

This project provides a toolset for scraping articles by author from the [EconLog](https://www.econlib.org/econlog/) website. This scraper is tailored to extract detailed article information, including HTML content, word counts, textual data, and embedded links. While the primary focus of this repository is to enable users to collect and save data for further analysis, some examples are in the [notebooks](/notebooks/) folder.

#### Core Objectives
1. Efficient Data Collection: Faciliatate the automated collection of articles from EconLog, categorized by authors, to streamline text analysis.
2. Rich Data Extraction: Retrieve a set fo data points for each article, encompassing the full HTML content, word counts, pure text, and embedded links within articles.
3. Versatility: While the primary aim is data acquisition, the toolset supports a wide range of secondary analyses, including topic analysis, text mining, and trend identification.

#### Ideal for:
1. Sentiment analysis or topic modeling.
2. Exploring trends, themes, and evolution of discourse within articles.

*Disclaimer*: No permissions were granted by the organization to scrape or otherwise use their data. Good luck.

## Table of Contents
- [Installation](#installation)
- [How to Use](#how-to-use)
- [License](#license)

## Installation

Clone repository: ``git clone https://github.com/gfbarbieri/econlog_article_scraper.git``

Check requirements: ``put requirements.txt here``

## How to Use

#### Example: Obtain a list of published authors.
```python
from scraper import EconlogScraper

# Intantiate EconLogScraper with default author.
els = EconlogScraper()

# Request all authors publised on EconLog.
print(els.request_authors())
```

#### Example: Extract an article's text.
```python
from scraper import EconlogScraper

# Define EconLog article.
article_url = 'https://econlib.org/econlog/article-name-here'

# Intantiate EconLogScraper with defaults.
els = EconlogScraper()

# Request article's contents and extract text.
p_tags, _ = els.request_article_content(url=article_url)
full_text = els.extract_article_text(article_content=p_tags)

# Print first 100 characters in the article.
print(full_text[:100])
```

#### Example: Extract text from all articles.
```python
from scraper import EconlogScraper

# Intantiate EconLogScraper with author.
els = EconlogScraper(author='author')

# Obtain the HTML container for every article published by the author.
containers = els.request_article_containers()

# Extract the URL from each container, request the content at the article's
# URL, extract text.
article_text = []

for container in containers:
    metadata = els.extract_article_metadata(article_container=container)
    p_tags, topics = els.request_article_content(url=metadata['url'])
    article_text.append(els.extract_article_text(article_content=p_tags))

# Print first article.
print(article_text[0])
```

#### Example: Extract all features from all articles and add to metadata.
```python
from scraper import EconlogScraper
from utils import text_utils

# Intantiate EconLogScraper with author.
els = EconlogScraper()

# Obtain the HTML container for every article published by the author.
containers = els.request_article_containers()

# Extract article metadata from each container.
metadata = [els.extract_article_metadata(article_container=container) for container in containers]

# Extract all features from each article.
for indx, article in enumerate(metadata):
    p_tags, topics = els.request_article_content(url=article['url'])
    full_text = els.extract_article_text(article_content=p_tags)
    embedded_urls = els.extract_embedded_urls(article_content=p_tags)
    word_count, word_freq = text_utils.word_counter(document=full_text)

    article['text'] = full_text
    article['topics'] = topics
    article['embedded_urls'] = embedded_urls
    article['word_count'] = word_count
    article['word_freq'] = word_freq

# Show example.
print(metadata[0])
```