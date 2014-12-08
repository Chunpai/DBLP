#!/usr/bin/python
#extract all author from inProceeding.xml, and build a dictionary with author name as key and index value by using 2014 inproceedings.xml.
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
        self.authorName = ''
        self.index = 0
        self.authors_dict = {} #author name is key, [index,paper_count] is value
        self.outfile = codecs.open('data/authors.txt','w','utf-8')
        self.outfile.write('index_number | author_name\n')

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
        elif name == 'author':
            if self.authorName not in self.authors_dict:
                self.index += 1
                self.authors_dict[self.authorName] = self.index
                self.outfile.write(str(self.index)+'|')
                self.outfile.write(self.authorName + '\n')
            self.isAuthor = 0
            self.authorName = ''
    
    #write content in <author> and </author>
    def characters(self,content):
        if self.isAuthor == 1:     
            if not content.isspace():
                #if content not in self.authors_dict:
                    #self.authors_dict[content] = self.index
                    #self.index += 1
                    #self.outfile.write(str(self.index)+'|')
                    #self.outfile.write(content + '\n')
                self.authorName += content


    
    #write the ending file tag for inProceeding.xml and close the written file
    def close_file(self):
        self.outfile.close()
        return self.authors_dict

def build_authors_dict():
    inProceedings = inProceedingsHandler()
    source = open('data/2014/inproceedings.xml','r')
    xml.sax.parse(source, inProceedings)
    authors_dict = inProceedings.close_file()
    return authors_dict


