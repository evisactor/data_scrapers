from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib2

import MYSQLdb
db=MySQLdb.connect("dbHost", "dbUser", "dbPass", "TargetdB")
cursor=db.cursor()




logfile=file("logfile.txt", 'a')


class Ref(object):
    def __init__(self, headline, date, text, url, last_modified):
        self.h=headline
        self.d=date
        self.t=text
        self.u=url
        self.m=last_modified

    
    def __repr__(self):
        h_str="headline:" + self.h + ","
        d_str="date:" + self.d + ","
        t_str="text:" + self.t + ","
        u_str="url:" + self.u, ","
        m_str="last modified:" + self.m
        return h_str + "\n" + d_str + "\n" + t_str + "\n" + u_str + "\n" + m_str + "\n"
    
    def __str__(self):
        h_str="headline:" + self.h + ","
        d_str="date:" + self.d + ","
        t_str="text:" + self.t + ","
        u_str="url:" + self.u + ","
        m_str="last modified:" + self.m
        
        return h_str + "\n" + d_str + "\n" + t_str + "\n" + u_str + "\n" + m_str + "\n"


def utc_to_est(date):
    foo=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S-04:00")
    timestamp = time.mktime(foo.timetuple())
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
    
 
def sql_insert(head, date, text, url):
    sql="INSERT INTO ARTICLES(HEADLINE, DATE, BODY, URL)VALUES('%s', '%s', '%s', '%s')" %(head, date, text, link)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        
data={}

def find_child_data(url):
    child=BeautifulSoup((urllib2.urlopen(link)).read())
            
    #scrape create-time from metatag
    date=child.find(attrs={'name': 'dcterms.created'})
    date=utc_to_est(date['content'])
            
    #time-modified number. Only if required.
    modified=child.find(attrs={'name': 'dcterms.modified'})
    modified=utc_to_est(modified['content'])
           
    #scrape + clean up the body of text
    body=child.find("div", attrs={'class': "copy"})
    body=text.get_text()
    body=body.encode('ascii', 'ignore')
    
    return date, modified, body         

while(1):
    logfile.write("logtime: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    logfile.write("Articles Scraped:\n")    
    soup=BeautifulSoup((urllib2.urlopen("http://nation.foxnews.com/")).read())
    block_news=soup.find_all("a", attrs={'class':'a-3'})
    block_top=soup.h2.a


    for news in block_top:
        link=news['href']
        head=news.contents[0]
        if head not in data:
            date, modified, body=find_child_data(link)
            
            #create object of Ref with these attributes
            href=Ref(head, date, body, link, modified)

            sql_insert(head, date, body, link)
           
            #for testing + debugging:
            logfile.write(date+","+ head+"\n")
            print "ok top"
        
    for news in block_news:
        #retrieve headline
        head=news.contents[0]
        head=head.encode('ascii', 'ignore')
        #retrieve url
        link=news['href']

        if head not in data:
            date, modified, body=find_child_data(link)
            href=Ref(head, date, body, link, modified)

            sql_insert(head, date, body, link)
           
            #for testing + debugging:
            logfile.write(date+","+ head+"\n")
            print "ok"
    
    
    
    s=raw_input("Press Enter to fetch again or type (q) to quit...")
    if s=="q":
        break
        
db.close()
    
    
