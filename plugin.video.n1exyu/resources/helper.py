from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse

class Article(object):
    title = ""
    thumb = ""
    url = ""

class ShowInfo(object):
    webPage = ''
    title = ''
    fanartUrl = ''
    iconUrl = ''
   

def get_show_data(show_web_page):
    
    webpage = urllib2.urlopen(show_web_page)
    soup = BeautifulSoup(webpage, "html.parser")
    media_div = soup.find('div', class_="medium-media")
    articles = media_div.find_all('article')

    toRet = []
    for a in articles:
        item = Article()
        
        h1 = a.find('h1')
        if h1 == None:
            continue
        item.title = h1.getText()

        img = a.find('img')
        if img == None:
            continue
        item.thumb = img.get('src')

        url = a.find('a')
        if a == None:
            continue
        url = url.get('href')
        item.url = find_youtube_id(url)

        print ">>>>>>>>>  " + item.thumb
        toRet.append(item)
        
    return toRet
    

def find_youtube_id(url):
    webpage = urllib2.urlopen(url)
    soup = BeautifulSoup(webpage, "html.parser")
    iframe = soup.find_all('iframe', class_="video-player")
    if iframe == None:
        return None
    return video_id(iframe[0].get('src'))

def video_id(yt_url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(yt_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def testPrint():
    print "----SUC"
    return;
