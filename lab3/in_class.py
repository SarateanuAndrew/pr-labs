import requests
from bs4 import BeautifulSoup

url = 'https://999.md/ro/list/real-estate/apartments-and-rooms'
prefix = 'https://999.md'
response = requests.get(url)


def parse(local_url):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href not in urls and  str(href).startswith('/ro/'):
                urls.append(prefix + href)
        print(*urls, sep='\n')
    else:
        print(f"Can't scrape the web page: {response.status_code}")

def recurse_pages(max_pages):
    if max_pages == 1:
        parse(url)
        return
    else:
        parse(url + '?page=' + str(max_pages))
        recurse_pages(max_pages - 1)

recurse_pages(5)