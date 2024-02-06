from collections import Counter

def extract_embedded_urls(article):
    """
    Extract the URLs embedded in article text, defined by 'p' tags. Returns a list of URLs.
    """
    embedded_urls = set()

    for p_tag in article:
        urls = p_tag.find_all('a')

        for url in urls:
            embedded_urls.add(url.get('href'))

    return embedded_urls

def extract_article_text(article):
    """
    Extract the article's text from the 'p' tags.
    
    Return a document (string).
    """
    text = []

    for p_tag in article:
        text.append(p_tag.text)

    return " ".join(text)

def word_counter(document):
    """
    Count the number of words in a document, return total count
    and counts by word (word frequency).
    """

    document = document.replace("'",'')
    document = document.lower()
    document = document.split()

    word_freq = Counter(document).most_common()
    word_count = Counter(document).total()

    return word_count, word_freq