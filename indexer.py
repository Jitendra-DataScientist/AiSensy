##### RAG Module #####
import os
# Imports the sys module to access command-line arguments
import sys
# Filters warnings
import warnings
# Imports the listdir, isfile, join, and isdir functions from the os and os.path modules to handle directories and files
from os import listdir
from os.path import isdir, isfile, join
# Imports the docx module to handle Word files
# import docx
# Imports the PyPDF2 module to handle PDF files
# import PyPDF2
# Imports the HuggingFaceEmbeddings class from the langchain_huggingface package to create embeddings
from langchain_huggingface import HuggingFaceEmbeddings
# Imports the Qdrant class from the langchain_qdrant package to create a Qdrant instance and send data to the vector database
from langchain_qdrant import Qdrant
# Imports the TokenTextSplitter class from the langchain_text_splitters package to split text into tokens
from langchain_text_splitters import TokenTextSplitter
# Imports the Presentation module from the pptx package to handle PowerPoint files
# from pptx import Presentation
# Imports the QdrantClient, Distance, and VectorParams classes from the qdrant_client package
# We'll create the Qdrant client and define storage parameters for the vector database
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from scrapper import Scrapper
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
file_handler = logging.FileHandler(os.path.join(log_directory, "indexer.log"))
file_handler.setLevel(logging.DEBUG)  # Set the logging level for this handler

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


warnings.filterwarnings('ignore')




class Indexer:

    def __init__(self):
        try:
            # Defines the model name to be used for creating embeddings
            model_name = "sentence-transformers/msmarco-bert-base-dot-v5"

            # Defines the model configuration
            model_kwargs = {'device': 'cpu'}

            # Defines the encoding configuration
            encode_kwargs = {'normalize_embeddings': True}

            # Initializes the HuggingFace embeddings class
            hf = HuggingFaceEmbeddings(model_name=model_name,
                                    model_kwargs=model_kwargs,
                                    encode_kwargs=encode_kwargs)

            # Initializes the Qdrant client
            client = QdrantClient("http://localhost:6333")

            collection_name = "AiSensy"

            # If the collection already exists, deletes it
            if client.collection_exists(collection_name):
                client.delete_collection(collection_name)

            # Creates a new collection with specified parameters
            client.create_collection(collection_name,
                                    vectors_config=VectorParams(size=768, distance=Distance.DOT))

            # Initializes the Qdrant instance
            self.qdrant = Qdrant(client, collection_name, hf)
        except Exception as init_error:  # pylint: disable=broad-exception-caught
            exception_type, _, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            logger.error("%s||||%s||||%s||||%d", exception_type, init_error, filename, line_number)


    # Defines the main function for indexing documents
    def main_indexing(self, scrape_urls_res, scrapper_obj):
        try:
            # Prints a message indicating that url content indexing is starting
            print("\nStarting Indexing...\n")

            # Iterates over each file in the list
            for key in scrape_urls_res:
                if key in scrapper_obj.list_ingested_urls():
                    print (f"url's content already indexed: {key}")
                    continue  ## the content has already been indexed
                try:
                    file_content = scrape_urls_res[key]

                    # Initializes the text splitter with specified chunk size and overlap
                    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)

                    # Splits the file content into text chunks
                    texts = text_splitter.split_text(file_content)

                    # Creates metadata for each text chunk
                    # This allows the LLM to reference the source
                    metadata = [{"path": key} for _ in texts]

                    # Adds the texts and their metadata to Qdrant
                    self.qdrant.add_texts(texts, metadatas=metadata)

                    scrapper_obj.append_to_ingested_urls(key)
                    print (f"Indexed for url: {key}")

                except Exception as e:

                    # If an error occurs, prints an error message
                    print(f"Process failed for url {key}: {e}")
                    print(f"Following were the scrapped contents {scrape_urls_res[key]}")

            # Prints a message indicating that indexing is complete
            print("\nIndexing Complete!\n")
        except Exception as main_indexing:  # pylint: disable=broad-exception-caught
            exception_type, _, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            logger.error("%s||||%s||||%s||||%d", exception_type, main_indexing, filename, line_number)



if __name__ == "__main__":

    scrapper_obj = Scrapper()
    indexer_obj = Indexer()


    urls = ["https://example.com"]
    to_be_ingested = scrapper_obj.ingestion_check(urls)
    scraped_content = scrapper_obj.scrape_urls(to_be_ingested)
    if not scraped_content:
        print (f"urls already ingested: {urls}")
    else:
        indexer_obj.main_indexing(scrape_urls_res = scraped_content, scrapper_obj = scrapper_obj)

    urls = ["https://example.com", "https://www.python.org"]
    to_be_ingested = scrapper_obj.ingestion_check(urls)
    scraped_content = scrapper_obj.scrape_urls(to_be_ingested)
    if not scraped_content:
        print (f"urls' contents already indexed: {urls}")
    else:
        indexer_obj.main_indexing(scrape_urls_res = scraped_content, scrapper_obj = scrapper_obj)

    urls = ["https://example.com", "https://www.python.org"]
    to_be_ingested = scrapper_obj.ingestion_check(urls)
    scraped_content = scrapper_obj.scrape_urls(to_be_ingested)
    if not scraped_content:
        print (f"urls' contents already indexed: {urls}")
    else:
        indexer_obj.main_indexing(scrape_urls_res = scraped_content, scrapper_obj = scrapper_obj)

