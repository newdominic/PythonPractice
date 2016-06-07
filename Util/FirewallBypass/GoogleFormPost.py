import requests

url = 'https://docs.google.com/forms/d/1lc_aB8iXXmeu0Ubz3o2wY-ByRfUmiNTF_-ZJmmam-OQ/formResponse'

post_data = {'entry.1820124651': 'content'}

requests.post(url, data=post_data)