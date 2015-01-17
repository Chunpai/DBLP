# scrap the microsoft academic research to get top-100 authors information for each subfield in CS
# get all authors' keywords as author_keywords.txt
from bs4 import BeautifulSoup
import requests
import codecs
import multiprocessing as mp

def authors_keywords(): 

    for subDomainID in range(23,25):
        outfile = codecs.open('keywords/'+str(subDomainID)+'authors_keywords.txt','w','utf-8')
        r = requests.get("http://academic.research.microsoft.com/RankList?entitytype=2&topDomainID=2&subDomainID="+ str(subDomainID) +"&last=0&start=1&end=100")
        soup = BeautifulSoup(r.content)
        #print soup.prettify()
        for item in soup.find_all("div",{"class":"content-narrow"}):
            link = item.find("a")
            #outfile.write(link.text + '|' + link['href'] + '\n')
            outfile.write(link.text+'|')
            id = link['href'].strip().split('/')[-2]
            count = 0
            for start in range(0,20):
                r2 = requests.get('http://academic.research.microsoft.com/Detail?entitytype=2&searchtype=9&id='+id+'&start='+str(start*10+1)+'&end='+str((start+1)*10))
                soup2 = BeautifulSoup(r2.content)
                for item2 in soup2.find_all("div",{"class":"title"}):
                    #print 'http://academic.research.microsoft.com/Detail?entitytype=2&searchtype=9&id='+id+'&start='+str(start*10+1)+'&end='+str((start+1)*10)
                    link2 =  item2.find("a")
                    outfile.write(link2.text+'|')
                    count += 1
            if count != 200:
                print "ERROR"
                print str(count)
            outfile.write('\n')
    outfile.close() 


if __name__ == "__main__":
    authors_keywords()
    """
    processes = [mp.Process(target=authors_keywords, args=(subDomainID,)) for subDomainID in range(2,13)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()
    """
