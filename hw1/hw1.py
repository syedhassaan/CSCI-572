from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json, ast
import csv 

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
 @staticmethod
 def search(query, sleep=True):
    if sleep: # Prevents loading too many pages too soon
        time.sleep(randint(10, 100))
    temp_url = '+'.join(query.split()) #for adding + between words for the query
    url = 'https://html.duckduckgo.com/html/?q=' + temp_url
    #url = 'https://www.duckduckgo.com/?q=' + temp_url
    print("Final URL: ", url)
    soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).content, "html.parser")
    # print("soup: ", soup.prettify())
    # for link in soup.find_all('a'):
    #     print("Link: ", link.get('href'))
    new_results = SearchEngine.scrape_search_result(soup)
    return new_results
 
 @staticmethod
 def scrape_search_result(soup):
    results = set()
    #implement a check to get only 10 results and also check that URLs must not be duplicated
    for link in soup.find_all('a'):
        if link.get('href') != None and link.get('href') != u'/html/':
            results.add(link.get('href'))
        if len(results) >= 10:
            #print("Max limit reached")
            break
    # print("results: ", results)

    return results

####### to create the json file #######
# f = open("100QueriesSet4.txt", "r")
# dict = {}
# for x in f:
#     search_result = list(SearchEngine.search(x))
#     dict[x] = search_result    

# with open('hw1.json', 'w') as f:
#     json.dump(dict, f)

####### to read the json file #######
f = open ('hw1.json', "r")
duckduckgo = json.loads(f.read())

#task 2
f = open ('Google_Result4.json', "r")
google = json.loads(f.read())

matching_items = {}

for key, value1 in duckduckgo.iteritems():
    value2 = google[key.encode("ascii")]
    #need to clean a bit i.e remove slash at end and http/https at the start
    d = [value for value in value1 if value in value2] # 2,3 
    matching_items[key] = d

# for key,value in matching_items.iteritems():
#     print(key, sum(1 for v in value if v))

fields = ['Queries', 'Number of Overlapping Results', 'Percent Overlap', 'Spearman Coefficient']
filename = "hw1.csv"
with open (filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields)
    #write a for loop here to write data to the csv file
    query_number = 0
    for key,value in matching_items.iteritems():
        query_number += 1
        matches = sum(1 for v in value if v)
        if matches == 0:
            spearman = 0
        elif matches == 1:
            if duckduckgo[key].index(value[0]) == google[key].index(value[0]):
                spearman = 1
            else:
                spearman = 0
        else:
            d2 = 0
            for v in value:
                # print("key: ", key)
                # print("v: ", v)
                # print("duckduckgo[key]: ", duckduckgo[key])
                # print("google[key]: ", google[key])
                # print("duckduckgo[key].index(v): ", duckduckgo[key].index(v))
                # print("google[key].index(v): ", google[key].index(v))
                d2 +=  (duckduckgo[key].index(v) - google[key].index(v))**2
            spearman = 1 - ( (6*d2) / ((matches*(pow(matches, 2)))-1))

        csvwriter.writerow(["Query " + str(query_number), matches, float((matches*100)/10), spearman])