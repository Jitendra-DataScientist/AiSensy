import os
import sys
import requests
from bs4 import BeautifulSoup
import json
import logging


# Determine the directory for logs
log_directory = os.path.join(os.getcwd(), 'logs')

# Create the logs directory if it doesn't exist
if not os.path.exists(log_directory):
    os.mkdir(log_directory)

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler for this script's log file
file_handler = logging.FileHandler(os.path.join(log_directory, "scrapper.log"))
file_handler.setLevel(logging.DEBUG)  # Set the logging level for this handler

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


class Scrapper:

    def __init__(self):
        self.ingested_urls = []


    def list_ingested_urls(self):
        return self.ingested_urls


    def append_to_ingested_urls(self, url):
        self.ingested_urls.append(url)


    def ingestion_check(self,url_list):
        return [url for url in url_list if url not in self.ingested_urls]


    def scrape_urls(self, url_list):
        try:
            scraped_data = {}
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

            for url in url_list:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

                    soup = BeautifulSoup(response.text, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)  # Extract text content

                    scraped_data[url] = text
                except requests.exceptions.RequestException as e:
                    scraped_data[url] = f"Error: {e}"
            
            return scraped_data
        except Exception as scrape_error:  # pylint: disable=broad-exception-caught
            exception_type, _, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            logger.error("%s||||%s||||%s||||%d", exception_type, scrape_error, filename, line_number)



if __name__ == "__main__":

    obj = Scrapper()

    urls = ["https://example.com"]
    to_be_ingested = obj.ingestion_check(urls)
    scraped_content = obj.scrape_urls(to_be_ingested)
    print (json.dumps(scraped_content, indent=4))
    # if not scraped_content:
    #     print (f"urls already ingested: {urls}")
    # else:
    # obj.main_indexing(scrape_urls_res = scraped_content)

    urls = ["https://example.com", "https://www.python.org"]
    to_be_ingested = obj.ingestion_check(urls)
    scraped_content = obj.scrape_urls(to_be_ingested)
    print (json.dumps(scraped_content, indent=4))
    # if not scraped_content:
    #     print (f"urls' contents already indexed: {urls}")
    # else:
    # obj.main_indexing(scrape_urls_res = scraped_content)

