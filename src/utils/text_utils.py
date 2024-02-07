from collections import Counter

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