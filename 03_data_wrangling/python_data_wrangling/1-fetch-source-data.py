import requests
from bs4 import BeautifulSoup

check_url = 'https://digital.nhs.uk/data-and-information/publications/statistical/nhs-workforce-statistics'
file_source_url = 'https://digital.nhs.uk'

response = requests.get(check_url)

soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

for link in links:
    print(link.get('href'))