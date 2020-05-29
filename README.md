A small side project of mine that scrapes the GoodReads.com quotes pages for a random quote of the day.

## Setup
This repo is tested on Python 3.8+

Install the following python packages via `pip install --user package_name`.
* bs4
* requests
* google-api-python-client 
* google-auth-httplib2 
* google-auth-oauthlib
* urllib
* flask
* flask-socketio

## Usage
Run the server via `python server.py`.

Server will be run on [the default local host at port 5000.](https://127.0.0.1:5000)

## Todo
|Goal|Additional Description|
|----|----------------------|
|Text orientation|Finds the clearest position of the background to display text at|
|True Quote of the Day|Pseudorandomness based on the date|
