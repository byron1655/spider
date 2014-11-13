from sgmllib import SGMLParser
import re
import urllib

class UrlLister(SGMLParser):
    is_a = ""
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_a = ""
        self.urls = []
        self.names = []
    def reset(self):
        self.is_a = ""
        self.urls = []
        self.names = []
        SGMLParser.reset(self)
    def start_a(self, attrs):
        self.is_a = 1
        href = [v for k, v in attrs if k=='href']
        if href:
        self.urls.extend(href)
    def end_a(self):
        self.is_a = ""
    def handle_data(self, text):
        if self.is_a:
            self.names.append(text)

def getPageContent(url):

    h = urllib.urlopen(url)

    return h.read()

content = getPageContent("http://news.163.com")


def getPageLinks(content):
	lister = UrlLister()
	lister.feed(content)
	#links = re.findall(']*?href=.*?<\/a>',content,re.I)

	item = []
	i = 0
	print len(lister.urls),len(lister.names)
	print lister.urls
	for url in lister.urls:
		i = lister.urls.index(url)

		#name = lister.names[i].decode('gbk').encode('utf8')
		#item[0] = url
		#item[1] = name

		#print item

	#return name

getPageLinks(content)