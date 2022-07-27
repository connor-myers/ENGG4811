import requests

def get_javadoc_html(url):
    return requests.get(url).text
