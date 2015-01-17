#get top-5000 keywords from all 24 subDomain of cs in Microsoft academic search
from bs4 import BeautifulSoup
import requests
import codecs



infile = open('subDomain/subDomain.txt','r')
subDomain_dict = {}
for line in infile:
    fields = line.strip().split("|")
    subDomain_dict[fields[0]] = fields[1]
infile.close()

#r = requests.get("http://academic.research.microsoft.com/?SearchDomain=2&SubDomain=7&entitytype=2")
for subDomainID in range(1,25):
    outfile = codecs.open('subDomain/'+subDomain_dict[str(subDomainID)]+'.txt','w','utf-8')
    for start in range(0,50):        
        r = requests.get("http://academic.research.microsoft.com/RankList?entitytype=8&topDomainID=2&subDomainID="+ str(subDomainID) +"&last=0&start="+str(start*100+1)+"&end="+str((start+1)*100))
        soup = BeautifulSoup(r.content)
        #print soup.prettify()
        for item in soup.find_all("td",{"class":"rank-content"}):
            #author_info = []
            #for link in item.find_all("a"):
            #    outfile.write(link.text + '|')
                #author_info.append( link.text )
            outfile.write(item.find("a").text + '\n')
    outfile.close() 
