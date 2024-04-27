import requests
from bs4 import BeautifulSoup
url = "http://x.com"
response = requests.get(url)
#with open('json_file', 'w') as f:
#    f.write(response.text)
soup = BeautifulSoup(response.text, 'lxml-xml')
