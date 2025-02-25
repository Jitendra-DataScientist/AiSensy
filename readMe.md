# Few points to note:

- It is hosted on "http://125.63.120.194:8008/".
- The web interface is built using streamlit, and not JS.
- I am not that proficient in JS, though I know it, and can make a simple user interface for this assignment.
- I am gradually building a web interface using JS, that I would be pushing to this repo gradually.

# For running this app locally (you could DIRECTLY use the link in the 2nd bullet point ABOVE):

- Clone this repo's main branch (any changes in instructions for running from other branches will be mentioned in the repective branch's readme).
- create a docker container for hosting the qdrant vector DB using the command: "docker run --name vectordb -dit -p 6333:6333 qdrant/qdrant"
- create a NVIDEA API key for "meta/llama-3.3-70b-instruct" from "https://build.nvidia.com/meta/llama-3_3-70b-instruct" after logging in (you get free 1000 credits per email ID).
- point working directory inside the repo. create a folder called "config". Inside "config" folder, create a python file "env_var.py", that holds the API key in the variable "nvidia_key", like this:
nvidia_key = "your_NVIDEA_key"
- Point the working directory to the outside config folder to just inside the repo.
- Run the api either by:
	- Run the API using python script command for which would be "python start_api.py". One could change port and host parameters inside the script.
	- Run the API using the command: "uvicorn api:app --reload --host 0.0.0.0 --port 8018". One could avoid the host parameter, one could use some other port, the default port is 8000, reload argument could also be skipped.
- Get the domains from the logs of the above command, and change the API's domain and port in line numbers 4 and 5 in web_app.py.
- Run the web_app using the command: "streamlit run web_app.py"
- In order to run the streamlit app on a custom port apart from the default 8501, use the "server.port" argument, for example: "streamlit run web_app.py --server.port 4200".

 # Key Improvements:

- improved UI.
- better error handling in source code.
- better error logging in source code.
