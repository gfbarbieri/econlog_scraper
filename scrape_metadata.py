from scraper_tools import request_containers, extract_authors, extract_years, extract_metadata
import pickle

# Find authors published on EconLog.
published_authors = extract_authors()

# Find all of the years in which the author published at least one article.
author = published_authors['Caplan, Bryan']
published_years = extract_years(author=author)

# Compile the metadata from each published article in a given year.
article_metadata = dict()
for year in published_years:
    print(year)
    html_containers = request_containers(author=author, year=year)

    container_metadata = []
    for container in html_containers:
        container_metadata.append(extract_metadata(container=container))

    article_metadata[year] = container_metadata

# Export article metadata.
with open('article_metadata.pickle', 'wb') as f:
    pickle.dump(article_metadata, f)
