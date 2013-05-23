import threading
import urllib2
from bs4 import BeautifulSoup

focus_words=['estimate', 'computer', 'growth'];

class downloadThread(threading.Thread):
    def __init__(self, threadID, URL, counter):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.URL=URL
        self.counter=counter
        
    def run(self):
        print "Starting download thread" + str(self.counter);
        downloadIndex(self.URL)
        print "Finished download and parse"
        
        
        
#removes all tags and non-ascii characters from html file
def cleaner(html_file):
    soup=BeautifulSoup(html_file)
    clean_string=''.join(soup.findAll(text=True))
    return clean_string
    
def parser(input_string):

#some key words to test for
    ans1=input_string.count('estimate')
    ans2=input_string.count('computer')
    ans3=input_string.count('growth')
    
    return ans1, ans2, ans3
    
        
def downloadIndex(file_URL):
    file_foo=urllib2.urlopen("ftp://ftp.sec.gov/"+file_URL);
    input=cleaner(file_foo.read())
    print parser(input)
    
 #some test samples
thread1=downloadThread(1, "edgar/data/1000045/0001193125-07-031642.txt", 1)
thread2=downloadThread(2, "edgar/data/1000045/0001144204-07-002274.txt", 2)


thread1.start()
thread2.start()
    