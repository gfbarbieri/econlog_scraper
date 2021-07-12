from scraper_tools import request_article
import pickle
import json

# Import article metadata.
with open('article_metadata.pickle', 'rb') as f:
    article_metadata = pickle.load(f)

# From the article metadata, extract articles content for text analysis.
article_content = []

for year, articles in article_metadata.items():
    print(year)
    for index, article in enumerate(articles):
        content, label = request_article(url=article['url'])

        # Add label, content number of embedded urls to article_metadata
        article_metadata[year][index]['label'] = label
        article_metadata[year][index]['content'] = content

# Export article metadata.
with open('article_content.pickle', 'w') as f:
    json.dumps(article_metadata, f, default=str)
