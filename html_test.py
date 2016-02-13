from HTMLParser import HTMLParser
import urllib2

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundPDFs = False
        self.current_set = ""
        self.pdf_map = {}
    def handle_starttag(self, tag, attrs):
        if len(attrs) < 1: 
            return
        if "http://www.hepforge.org/archive/lhapdf/pdfsets" in attrs[0][1]:
            if not self.foundPDFs:
                self.foundPDFs = True
            else: 
                self.pdf_map[self.current_set]["path"] = attrs[0][1]
    def handle_data(self, data):
        if "Notes" in data:
            self.foundPDFs = True
            return
        if self.foundPDFs:
            if data.isdigit():
                self.pdf_map[data] = {}
                self.current_set = data
            elif self.current_set in self.pdf_map.keys():
                self.pdf_map[self.current_set]["name"] = data
    def get_pdfs(self):
        return self.pdf_map

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

response = urllib2.urlopen('https://lhapdf.hepforge.org/pdfsets.html')
info = response.read()
parser.feed(info)

pdf_map = parser.get_pdfs()
