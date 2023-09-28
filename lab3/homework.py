import requests
from bs4 import BeautifulSoup
import re

def parse(Url):
    response = requests.get(Url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        details = []
        li_elements = soup.find_all('li', class_='m-value')
        for li in li_elements:
            key = li.find('span', class_='adPage__content__features__key').text.strip()
            value = li.find('span', class_='adPage__content__features__value').text.strip()

            details.append(key + ": "+ value)

        return details

print(*parse("https://999.md/ro/84319878"), sep='\n')