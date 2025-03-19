from bs4 import BeautifulSoup
import requests
import json

def filter_tags(tag):
    #to find the correct tag
    if tag.name == "a" and tag.get("data-track-action") == "view article":
        return True
    elif tag.name == "p" and tag.parent.get("data-test") == "article-description":
        return True
    elif tag.name == "div" and (tag.get("data-test") == "journal-title-and-link" or tag.get("data-test") == "volume-and-page-info"):
        return True
    elif tag.name == "span" and (tag.parent.get("itemprop") == "creator" or tag.parent.get("data-test") == "article.type"):
        return True
    return False

def filter_author(tag):
    #to find author tag
    if tag.name == "a" and tag.get("data-test") == "author-name":
        return True
    else:
        return False

url = 'https://www.nature.com/search?q=llm&page=1'
response = requests.get(url)
response.encoding = 'utf-8'
if response.status_code == 200:
    soup  = BeautifulSoup(response.text, 'lxml')
    a_txt = soup.prettify()
    with open('page1.txt', 'w', encoding='utf-8')as file:
            file.write(f"{a_txt}\n")
            file.close()
    print('page1.txt created')
else:   
    print('failed to request the page')

a_tag = soup.find_all(filter_tags)
list_paper = []
current_journal = None
current_paper = None
flag = False
for i in range(len(a_tag)): 
    a = a_tag[i]
    if(a.name == "a"):
        current_paper = {'title':a.get_text(), 'url' : a.get("href"), 'author' : []}
        flag = False
    elif(a.name == "p"):
        current_paper['descirption'] = a.get_text()
    elif(a.name == "div" and a.get("data-test") == "journal-title-and-link"):
        index = a.get_text()
    elif(a.name == "div" and a.get("data-test") == "volume-and-page-info"):
        current_paper['volume-and-page-info'] = a.get_text()
    elif(a.name == "span" and a.parent.get("itemprop") == "creator"):
        current_paper['author'].append(a.get_text())
    elif(a.name == "span" and a.parent.get("data-test") == "article.type"):
        current_paper['type'] = a.get_text()
    if(i == len(a_tag) - 1 or a_tag[i+1].name == "a"):
        if current_paper.get('descirption') == None:
            current_paper['description'] = "no description"
        for jour in list_paper:
            if jour.get("journal") == index:
                jour['papers'].append(current_paper.copy())
                flag = True
                break
        if not flag:
            list_paper.append({"journal": index, "papers":[current_paper.copy()]})
        current_paper = None

for jour in list_paper:
    print(f"{jour['journal']}:{len(jour['papers'])}")

for jour in list_paper:
    for article in jour['papers']:
        url = 'https://www.nature.com'+article['url']
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
        a_tag = soup.find_all(filter_author)
        author_list = []
        for a in a_tag:
            author_list.append(a.get_text())
        article['author'] = author_list.copy()
        author_list = None     

with open('nature_llm.json', 'w', encoding='utf-8')as file:
    json.dump(list_paper, file, indent=2, separators=(',',':'))
