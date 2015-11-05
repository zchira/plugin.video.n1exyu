from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse
from ytHelper import vids_by_playlist

NEXT_PAGE = "Next Page"
PREV_PAGE = "Previous Page"

class Article(object):
    title = ""
    thumb = ""
    yt_id = ""
    description = ""

    
class ShowInfo(object):
    webPage = ''
    title = ''
    fanartUrl = ''
    iconUrl = ''
    yt_playlist_id = '';

def get_show_data_yt(yt_playlist_id, nextpage = False):
    yt_response = vids_by_playlist(yt_playlist_id, nextpage)
    toRet = []
      
    try:
        prevPageToken = yt_response["prevPageToken"]
        prevPage = Article()
        prevPage.title = PREV_PAGE
        prevPage.yt_id = prevPageToken
        toRet.append(prevPage)
    except:
        pass
        
    for i in yt_response["items"]:
        item = Article()
        try:
            item.title = i["snippet"]["title"]            
            item.yt_id = i["snippet"]["resourceId"]["videoId"]
            item.thumb = i["snippet"]["thumbnails"]["high"]["url"]
            item.description = i["snippet"]["description"]
            toRet.append(item)
        except:
            pass

    try:
        nextPageToken = yt_response["nextPageToken"]
        nextPage = Article()
        nextPage.title = NEXT_PAGE
        nextPage.yt_id = nextPageToken
        toRet.append(nextPage)
    except:
        pass
    

        
    return toRet

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
        item.yt_id = find_youtube_id(url)

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

