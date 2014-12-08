# scrap the microsoft academic research to get top-100 authors information for each subfield in CS
# save the data at data/authors_info.txt
import mechanize
from bs4 import BeautifulSoup
import requests


def scrap_and_match(author_name):
#use mechanize to fill the form, submit and get the url to direct
    br = mechanize.Browser()
    url = "http://www.informatik.uni-trier.de/~ley/db/about/author.html"
    response = br.open(url)
    br.form = list(br.forms())[1] 
    for control in br.form.controls:
        if control.type == "text":
            control.value = author_name
    response = br.submit()
    url = response.geturl()

# use beautifulSoup to request the url and read the headline
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    item = soup.find("div",{"id":"headline"})
    return item.find("h1").text
