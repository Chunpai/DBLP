#!/usr/bin/python
#read authors_dict from authors.txt 
#also, will create a edgelist file. 
#use xml.sax, because it support external entity expansion
# attention: characters function will read content inconsistently, which means it will not parse whole content between tags at the same time
import xml.sax
import codecs
from xml.sax.saxutils import unescape
#from build_authors_dict import build_authors_dict


class inProceedingsHandler(xml.sax.handler.ContentHandler):
    # initialize an object for xml.sax.parse(source,handler)
    def __init__(self,authors_dict,year):
        #xml.sax.ContentHandler.__init__(self)
        self.isInProceedings = 0
        self.isAuthor = 0
        self.authorName = ''
        self.index = 0
        self.author_list  = [] #store authors for one paper
        self.authors_dict = authors_dict #author name is key, index is value
        self.outfile = open('data/partitions/'+str(year-3)+'_'+str(year)+'_edgelist.txt','w')

    #starting tag of an element, use this function to check the scanning position
    def startElement(self, name, attrs):
        if name == 'inproceedings':
            self.isInProceedings = 1
        if name == 'author':
            self.isAuthor = 1
    
    #ending tag of an element, use this function to check the scanning position
    def endElement(self,name):
        if name == 'inproceedings':
            self.isInProceedings = 0
            length = len(self.author_list)
            if length > 1:
                for i in range(1,length):
                    self.outfile.write(str(self.author_list[0])+ ' ' + str(self.author_list[i]) + '\n')
            self.author_list = []
        elif name == 'author':
            #self.authorName = self.authorName.decode('string_escape').decode("utf-8")
            if self.authorName in self.authors_dict:
                self.author_list.append(self.authors_dict[self.authorName])
            else:
                print self.authorName
                raise SyntaxError('dictionary error')
            self.isAuthor = 0
            self.authorName = ''
    
    #write content in <author> and </author>
    def characters(self,content):
        if self.isAuthor == 1:     
            if not content.isspace():
                #if content not in self.authors_dict:
                #    self.authors_dict[content] = [self.index,1]
                #    self.index += 1
                #    self.outfile1.write(str(self.index)+'|')
                #    self.outfile1.write(content + '\n')
                #    self.author_list.append(self.index)   # put author index into list for current paper
                #else:
                #if content in self.authors_dict: 
                #    self.author_list.append(self.authors_dict[content])
                #else:
                #    print self.authors_dict[content]
                #    raise SyntaxError('dictionary error')
                self.authorName += content
    
    #write the ending file tag for inProceeding.xml and close the written file
    def close_file(self):
        self.outfile.close()


if __name__ == '__main__':
    """
    """
    #authors_dict = build_authors_dict()
    for year in reversed(xrange(1994,2015,4)):
        authors_dict = {}
        infile = codecs.open('data/partitions/'+str(year-3)+'_'+str(year)+'_authors.txt','r','utf-8')
        infile.readline()
        for line in infile:
            fields = line.strip().split('|')
            if fields[1] not in authors_dict:
                authors_dict[fields[1]] = fields[0]
            else:
                print fields[1] , fields[0]
                print authors_dict[fields[1]]
        print len(authors_dict)
        inProceedings = inProceedingsHandler(authors_dict,year)
        source = open('data/partitions/'+str(year-3)+'_'+str(year)+'_inproceedings.xml','r')
        xml.sax.parse(source, inProceedings)
        inProceedings.close_file()
    

