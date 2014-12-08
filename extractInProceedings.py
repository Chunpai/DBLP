#!/usr/bin/python
#use xml.sax, because it support external entity expansion
#this program will extract all inproceedings elements in dblp.xml into inProceedings.xml
import xml.sax
import codecs
from xml.sax.saxutils import escape

# a handler class  for xml.sax.parse(source,handler)
class dblpHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        #xml.sax.ContentHandler.__init__(self)
        self.isProceedings = 0
        self.outfile = codecs.open('data/inProceedings.xml','w','utf-8')
        self.outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.outfile.write('<!DOCTYPE dblp SYSTEM "../dblp.dtd">\n')
        self.outfile.write('<dblp>\n\n')

    #starting tag of an element
    def startElement(self, name, attrs):
        if name == 'inproceedings':
            self.isProceedings = 1
            self.outfile.write('<inproceedings>\n')
        elif self.isProceedings == 1:
            self.outfile.write('<'+name+'>')
    
    #ending tag of an element
    def endElement(self,name):
        if name == 'inproceedings':
            self.outfile.write('</inproceedings>\n\n')
            self.isProceedings = 0
        elif self.isProceedings == 1:
            self.outfile.write('</'+name+'>\n')
    
    #write content in <inproceeding> and </inproceeding>
    def characters(self,content):
        if self.isProceedings == 1:     
            if not content.isspace():
                self.outfile.write(escape(content))

    #write the ending file tag for inProceeding.xml and close the written file
    def close_file(self):
        self.outfile.write('</dblp>')
        self.outfile.close()


if __name__ == '__main__':
    dblp = dblpHandler()
    source = open('data/dblp.xml','r')
    xml.sax.parse(source, dblp)
    dblp.close_file()
    

