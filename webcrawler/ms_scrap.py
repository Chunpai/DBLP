# scrap the microsoft academic research to get top-100 authors information for each subfield in CS
# save the data at data/authors_info.txt
from bs4 import BeautifulSoup
import requests
import codecs


outfile = codecs.open('original_authors_info.txt','w','utf-8')
#r = requests.get("http://academic.research.microsoft.com/?SearchDomain=2&SubDomain=7&entitytype=2")
for subDomainID in range(1,25):
    r = requests.get("http://academic.research.microsoft.com/RankList?entitytype=2&topDomainID=2&subDomainID="+ str(subDomainID) +"&last=0&start=1&end=100")
    soup = BeautifulSoup(r.content)
    #print soup.prettify()
    for item in soup.find_all("div",{"class":"content-narrow"}):
        author_info = []
        for link in item.find_all("a"):
            outfile.write(link.text + '|')
            #author_info.append( link.text )
        outfile.write('\n') 
    
outfile.close() 
