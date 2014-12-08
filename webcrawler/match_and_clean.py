# match the author name with the dblp data
# and make the name accord with each other
from bs4 import BeautifulSoup
import requests
import codecs
from dblp_scrap import scrap_and_match

infile1 = open("../data/authors.txt","r")
infile1.readline()
authors_dict ={}
for line in infile1:
    fields = line.strip().split('|')
    if fields[1] not in authors_dict:
        authors_dict[fields[1]] = fields[0]
infile1.close()

infile2 = open("hand_revised_authors_info.txt","r")
outfile = codecs.open('revised_authors_info.txt','w')
for line in infile2:
    fields = line.strip().split('|')
    if fields[0] not in authors_dict:
        dblp_author_name = scrap_and_match(fields[0])
        if dblp_author_name not in authors_dict:
            print fields[0]
            #raise SyntaxError
        else:
            fields[0] = dblp_author_name     
            for field in fields:
                outfile.write(field+'|')
            outfile.write('\n')
    else:
        outfile.write(line)

infile2.close()
outfile.close()
