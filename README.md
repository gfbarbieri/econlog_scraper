# Web Scraping EconLog Articles

### Project Overview
The goal is to explore the interconnectedness of blog posts by author Bryan Caplan on EconLog. Each article and the hyperlinks in the article represent a connected pair of nodes, from which a full network can be created.

### Web Scrape Article Content
See the Scrape_EconLog_Articles.ipynb.

1. Extract a list of authors that post on EconLog.
2. Extract a list of years the author published on EconLog. If my memory serves, EconLog chose to organize posts by year, so year must be looped over.
3. For each year, accumulate every articles metadata, including the title, date, author, and the articles URL.
4. For each article, extract the articles text, embedded URLs, and produce a word count.
5. Add the articles content to the articles metadata.
6. Save the final article contents.

### Analysis
See Article_Network.ipynb

1. Load article content.
2. Count total articles.
3. Plot articles per year.
4. Plot word count per article.
5. Create article network where each edge is an article URL and an embedded URL.

![Article Network](../figs/article_network.jpg)
