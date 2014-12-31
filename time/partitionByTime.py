#!/usr/bin/python
#use xml.sax, because it support external entity expansion
#this program will partition inproceedings.xml by year
import xml.sax
import codecs
from xml.sax.saxutils import escape
import multiprocessing as mp


# a handler class  for xml.sax.parse(source,handler)
class dblpHandler(xml.sax.handler.ContentHandler):
    def __init__(self,year):
        #xml.sax.ContentHandler.__init__(self)
        self.isInProceedings = 0
        self.buffer = '' 
        self.isYear = 0
        self.year = year
        self.currentYear = 0   # year for current parsing inproceeding paper
        #self.outfile = codecs.open('data/inProceedings.xml','w','utf-8')
        self.outfile = codecs.open('data/partitions/'+str(year-3)+'_'+str(year)+'_inproceedings.xml','w','utf-8')
        self.outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.outfile.write('<!DOCTYPE dblp SYSTEM "../dblp.dtd">\n')
        self.outfile.write('<dblp>\n\n')


    #starting tag of an element
    def startElement(self, name, attrs):
        if name == 'inproceedings':
            self.isInProceedings = 1
            #self.outfile.write('<inproceedings>\n')
            self.buffer += '<inproceedings>\n'
        elif self.isInProceedings == 1:    # name != inproceedings and isInProceedings == 1
            #self.outfile.write('<'+name+'>')
            self.buffer += '<'+name+'>'
            if name == 'year':
                self.isYear = 1

    #ending tag of an element
    def endElement(self,name):
        if name == 'inproceedings':
            #self.outfile.write('</inproceedings>\n\n')
            self.buffer += '</inproceedings>\n\n'
            if self.currentYear <= self.year and self.currentYear > (self.year - 4):    #if same to year 
                self.outfile.write(self.buffer)
            self.buffer = ''
            self.isInProceedings = 0
        elif self.isInProceedings == 1:
            #self.outfile.write('</'+name+'>\n')
            self.buffer += '</'+name+'>\n'
            if name == 'year':
                self.isYear = 0

    #write content in <inproceeding> and </inproceeding>
    def characters(self,content):
        if self.isInProceedings == 1:     
            if not content.isspace():
                #self.outfile.write(escape(content))
                self.buffer += escape(content)
        if self.isYear == 1:
            self.currentYear = int(content)

    #write the ending file tag for inProceeding.xml and close the written file
    def close_file(self):
        self.outfile.write('</dblp>')
        self.outfile.close()


def partition():
    for year in reversed(xrange(1994,2015,4)):
        dblp = dblpHandler(year)
        source = open('../data/2014/inproceedings.xml','r')
        xml.sax.parse(source, dblp)
        dblp.close_file()


if __name__  == "__main__":
    processes = [mp.Process(target=partition) for x in range(6)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()


