    __author__ = 'Daniel Murphy'

import mechanize
from bs4 import BeautifulSoup
import re

imdb = 'http://www.imdb.com'
user_search = raw_input('Please enter a search term:')
imdb_search = 'http://www.imdb.com/find?q='
search_url = imdb_search+user_search+'&s=tt'

#Replace any spaces in search term with a +
search_url = search_url.replace(' ', '+')

browser = mechanize.Browser()
#I added a header since some searches would return nothing if no header was specified. eg. searching for "this"
browser.addheaders = [('User-Agent', 'Mozilla/5.0')]
response = browser.open(search_url)
html = response.read()

soup = BeautifulSoup(html)

#Find all links from search page that are for media titles from first table
table = soup.find('table', class_='findList')
links = table.find_all(href=re.compile('title/tt'))

#Instantiating some lists
href1 = []
result_link = []

#Loop through list of links html and get hyperlinks
for link in links:
    href = link['href'].strip()
    href = imdb+href
    href1.append(str(href))

#Remove duplicate hyperlinks, since there are two for each result. One from the picture and one from text.
for i in href1:
    if i not in result_link:
        result_link.append(i)

#Make sure no more than ten links will be used.
result_link = result_link[:10]

result = []

#Loop through links, open each page and print release date and title.
for i in result_link:
    response = browser.open(i)
    html = response.read()
    soup = BeautifulSoup(html)
    titl = soup.find(class_='itemprop').text.strip()

    #Since the different pages don't always have the full release date
    # this tries to get full date otherwise just the year/years
    try:
        head = soup.find(class_='header')
        infobar = head.find(class_='nobr').text.strip()
    except:
        error = 'No date'
    try:
        infobar = soup.find(href=re.compile('/year/')).text.strip()

    except:
        error = 'No date'

    try:
        infobar = soup.find('a', {'title': 'See all release dates'}).text.strip()
        #Regex to remove country
        infobar = re.sub(r'\(.*?\)', '', infobar).strip()
    except:
        error = 'No date'

    temp_result = titl + ' : ' + infobar
    result.append(temp_result)

    #print titl, ' : ', infobar
    infobar = 'No Date on page'

#Show list of titles and release dates.
print result
