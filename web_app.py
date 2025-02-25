import os
import sys
import streamlit as st
import requests
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
file_handler = logging.FileHandler(os.path.join(log_directory, "web_app.log"))
file_handler.setLevel(logging.DEBUG)  # Set the logging level for this handler

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

try:
    api_domain = "http://125.63.120.194"
    api_port = "8018"

    INDEX_API_URL = f"{api_domain}:{api_port}/index"
    QUERY_API_URL = f"{api_domain}:{api_port}/api"

    st.title("URL-Based Q&A Tool")

    # Initialize session state
    if "urls" not in st.session_state:
        st.session_state["urls"] = []
    if "indexing_complete" not in st.session_state:
        st.session_state["indexing_complete"] = False

    # Function to add a URL input field
    def add_url():
        st.session_state["urls"].append("")
        st.rerun()  # Force UI update

    # Function to remove a URL input field
    def remove_url(index):
        del st.session_state["urls"][index]
        st.rerun()  # Force UI update

    # Section 1: URL Indexing
    st.header("URL Indexing")
    st.write("Enter URLs to be indexed:")

    # Dynamically generate input fields for URLs
    for i, url in enumerate(st.session_state["urls"]):
        cols = st.columns([4, 1])
        st.session_state["urls"][i] = cols[0].text_input(f"URL {i+1}", value=url, key=f"url_{i}")
        if cols[1].button("❌", key=f"remove_{i}"):
            remove_url(i)

    # Button to add new URL input field
    if st.button("➕ Add URL"):
        add_url()

    # Button to submit URLs for indexing
    if st.button("Submit URLs for Indexing"):
        # Filter out empty URLs before sending
        valid_urls = [url.strip() for url in st.session_state["urls"] if url.strip()]
        
        if valid_urls:
            payload = {"urls": valid_urls}
            response = requests.post(INDEX_API_URL, json=payload)
            if response.status_code in [200, 201]:
                st.session_state["indexing_complete"] = True
                st.success("Indexing complete!")
            else:
                st.error("Indexing failed. Try again.")
        else:
            st.error("Please enter at least one valid URL.")

    # Section 2: Query API (disabled until indexing completes)
    st.header("Ask a Question")
    query = st.text_input("Enter your query:", disabled=not st.session_state["indexing_complete"])
    if st.button("Submit Query", disabled=not st.session_state["indexing_complete"]):
        if query:
            response = requests.post(QUERY_API_URL, json={"query": query})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                st.write("**Answer:**", answer)
            else:
                st.error("Failed to fetch answer. Try again.")

except Exception as api_error:  # pylint: disable=broad-exception-caught
    exception_type, _, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    logger.error("%s||||%s||||%s||||%d", exception_type, api_error, filename, line_number)
    st.error("Error in application.")
