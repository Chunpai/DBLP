#!/usr/bin/python
#extract all author from inProceeding.xml, and build a dictionary with author name as key and index value by using 2014 inproceedings.xml.
#also, will create a edgelist file. 
#use xml.sax, because it support external entity expansion
import xml.sax
import codecs
from xml.sax.saxutils import unescape
import multiprocessing as mp

class inProceedingsHandler(xml.sax.handler.ContentHandler):
    # initialize an object for xml.sax.parse(source,handler)
    def __init__(self,authors_dict,year):
        #xml.sax.ContentHandler.__init__(self)
        self.isInProceedings = 0
        self.isAuthor = 0
        self.authorName = ''
        #self.index = 0
        self.year = year
        self.all_authors_dict = authors_dict
        self.current_authors_dict = {}
        self.outfile = codecs.open('data/partitions/'+str(year-3)+'_'+str(year)+'_authors.txt',"w","utf-8")
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
            if self.authorName in self.all_authors_dict:
                index = self.all_authors_dict[self.authorName]
                format_index = str(self.year-3)+str(self.year)+'{:07}'.format(int(index))
                if self.authorName not in self.current_authors_dict:
                    self.current_authors_dict[self.authorName] = format_index
                    self.outfile.write(format_index+'|')
                    self.outfile.write(self.authorName + '\n')
            else:
                raise SyntaxError("ERROR")
            self.isAuthor = 0
            self.authorName = ''
            """
            if self.authorName not in self.authors_dict:
                self.index += 1
                format_index = str(self.year-3)+str(self.year)+'{:07}'.format(self.index)
                self.authors_dict[self.authorName] = format_index
                self.outfile.write(format_index+'|')
                self.outfile.write(self.authorName + '\n')
            self.isAuthor = 0
            self.authorName = ''
            """
    
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
        #return self.authors_dict


def read_authors_dict():
    infile = codecs.open("data/all_authors.txt","r","utf-8")
    infile.readline()
    all_authors_dict = {}
    for line in infile:
        fields = line.strip().split('|')
        if fields[1] not in all_authors_dict:
            all_authors_dict[fields[1]] = fields[0]
    infile.close()
    return all_authors_dict


#build authors dict for each periods with format index
def build_authors_dict(all_authors_dict):
    for year in reversed(xrange(1994,2015,4)):
        inProceedings = inProceedingsHandler(all_authors_dict,year)
        source = open('data/partitions/'+str(year-3)+'_'+str(year)+'_inproceedings.xml','r')
        xml.sax.parse(source, inProceedings)
        inProceedings.close_file()


if __name__ == "__main__":
    authors_dict = read_authors_dict()
    processes = [mp.Process(target=build_authors_dict, args=(authors_dict,)) for x in range(6)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()
