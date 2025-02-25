import streamlit as st
import requests

api_domain = "http://125.63.120.194"
api_port = "8000"

INDEX_API_URL = f"{api_domain}:{api_port}/index"
QUERY_API_URL = f"{api_domain}:{api_port}/api"

st.title("API Interaction UI")

# Section 1: URL Indexing
st.header("URL Indexing")
url_inputs = []

if "urls" not in st.session_state:
    st.session_state["urls"] = []
if "indexing_complete" not in st.session_state:
    st.session_state["indexing_complete"] = False

def add_url():
    st.session_state["urls"].append("")

def remove_url(index):
    del st.session_state["urls"][index]

st.write("Enter URLs to be indexed:")

for i, url in enumerate(st.session_state["urls"]):
    cols = st.columns([4, 1])
    st.session_state["urls"][i] = cols[0].text_input(f"URL {i+1}", value=url, key=f"url_{i}")
    if cols[1].button("❌", key=f"remove_{i}"):
        remove_url(i)
        st.experimental_rerun()

if st.button("➕ Add URL"):
    add_url()

if st.button("Submit URLs for Indexing"):
    payload = {"urls": st.session_state["urls"]}
    response = requests.post(INDEX_API_URL, json=payload)
    if response.status_code in [200, 201]:
        st.session_state["indexing_complete"] = True
        st.success("Indexing complete!")
    else:
        st.error("Indexing failed. Try again.")

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
