#!/usr/bin/python
#extract all author from inProceeding.xml, and build a dictionary with author name as key and index and value.
#also, will create a edgelist file. 
#use xml.sax, because it support external entity expansion
import xml.sax
import codecs
from xml.sax.saxutils import unescape

class inProceedingsHandler(xml.sax.handler.ContentHandler):
    # initialize an object for xml.sax.parse(source,handler)
    def __init__(self):
        #xml.sax.ContentHandler.__init__(self)
        self.isInProceedings = 0
        self.isAuthor = 0
        self.index = 0
        self.author_list  = [] #store authors for one paper
        self.authors_dict = {}
        self.outfile1 = codecs.open('authors_dict.txt','w','utf-8')
        self.outfile1.write('index_number | author_name \n')
        self.outfile2 = open('test.edgelist','w')


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
                    self.outfile2.write(str(self.author_list[0])+ ' ' + str(self.author_list[i]) + '\n')
            self.author_list = []
        if name == 'author':
            self.isAuthor = 0
    
    #write content in <author> and </author>
    def characters(self,content):
        if self.isAuthor == 1:     
            if not content.isspace():
                if content not in self.authors_dict:
                    self.authors_dict[content] = self.index
                    self.index += 1
                    self.outfile1.write(str(self.index)+'|')
                    self.outfile1.write(content + "\n")
                    self.author_list.append(self.index)   # put author index into list for current paper
                else:
                    self.author_list.append(self.authors_dict[content])
    
    #write the ending file tag for inProceeding.xml and close the written file
    def close_file(self):
        self.outfile1.close()
        self.outfile2.close()


if __name__ == '__main__':
    inProceedings = inProceedingsHandler()
    source = open('test.xml','r')
    xml.sax.parse(source, inProceedings)
    inProceedings.close_file()
    

