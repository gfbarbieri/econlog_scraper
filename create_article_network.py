from scraper_tools import request_article, extract_urls
import pickle

# Import article metadata.
with open('article_metadata.pickle', 'rb') as f:
    article_metadata = pickle.load(f)

# Create a network between the article and the articles linked in the article. Specifically,
# create a list where each item is a node-pair. Source Article -> Target Article.
article_network = []

for year, articles in article_metadata.items():
    print(year)
    for index, article in enumerate(articles):
        content, label = request_article(url=article['url'])
        embedded_urls = extract_urls(article=content)

        for embedded_url in embedded_urls:
            article_network.append([article['title'], article['url'], embedded_url])

# Output article network.
with open('article_network.pickle', 'wb') as f:
    pickle.dump(article_network, f)
