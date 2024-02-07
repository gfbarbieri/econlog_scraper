from scraper import EconlogScraper
from utils import text_utils
from utils import data_io

def main():
    # Initialized scraper using defaults.
    print(f"Initialize scraper with default author.")
    els = EconlogScraper()
    print(f"Scraper initialized with author {els.author}.")

    # Request all of the article containers for the author. Returns a list
    # of HTML containers.
    print("Requesting article containers.")
    containers = els.request_article_containers()
    print(f"Article containers received: {len(containers)}")

    # Request the metadata from all article containers. Returns a list of
    # dictionaries.
    print("Extracting metadata for each container.")
    metadata = (
        [
            els.extract_article_metadata(article_container=container)
            for container in containers
        ]
    )
    print(f"Metadata extracted from {len(metadata)} containers.")

    # For each article: (1) request the article's content, including its
    # text and labels. From the text, (2) extract the raw text from HTML
    # tags and (3) any embedded urls from HTML tags. From the raw text, (4)
    # perform a word count and (5) get a word list.
    print("Requesting article contents and extracting features.")

    for indx, article in enumerate(metadata):
        print(f"{indx}: Starting article.")

        # 1. Request the article's content.
        print(f"{indx}: Requesting article content.")
        p_tags, topics = els.request_article_content(url=article['url'])

        # 2. Extract raw text from the HTML <p> tags.
        print(f"{indx}: Extracting raw text.")
        text = els.extract_article_text(article_content=p_tags)

        # 3. Extract embedded URLs from the HTML <a> tags. This is required
        # for the subsequent network analysis on embedded articles.
        print(f"{indx}: Extracting embedded URLs.")
        embedded_urls = els.extract_embedded_urls(article_content=p_tags)

        # 4. & 5. Count total and individual words.
        print(f"{indx}: Performing word counts.")
        word_count, word_freq = text_utils.word_counter(document=text)

        # Add to dictionary.
        print(f"{indx}: Adding results to metadata dictionary.")
        article['text'] = text
        article['topics'] = topics
        article['embedded_urls'] = embedded_urls
        article['word_count'] = word_count
        article['word_freq'] = word_freq

        print(f"{indx}: Article completed.")

    print("Completed all articles.")

    # Write (1) containers and (2) metadata to file.
    print(f"Writing data to file: {els.author}_article_containers.pkl, {els.author}_article_data.pkl")
    data_io.write_file(data=containers, file_name=f"{els.author}_article_containers.pkl")
    data_io.write_file(data=metadata, file_name=f"{els.author}_article_data.pkl")

if __name__ == '__main__':
    main()