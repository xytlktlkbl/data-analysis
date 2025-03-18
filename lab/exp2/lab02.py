from bs4 import BeautifulSoup
import requests
url = 'https://www.nature.com/search?q=llm&page=1'
response = requests.get(url)
response.encoding = 'utf-8'
if response.status_code == 200:
    soup  = BeautifulSoup(response.text, 'lxml')
    with open('page1.txt', 'w', encoding='utf-8')as file:
        file.write(soup.prettify())
        file.close()
    print('page1.txt created')
else:   
    print('failed to request the page')
