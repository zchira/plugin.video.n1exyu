import os
import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import resources.helper as helper
from resources.helper import Article
from resources.helper import ShowInfo

from resources.ytHelper import vids_by_playlist

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


my_addon = xbmcaddon.Addon("plugin.video.n1exyu")
iconImage = my_addon.getAddonInfo('icon')
fanart = my_addon.getAddonInfo('fanart')

LIVE_SERBIAN_URL = "http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1srb&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0"
LIVE_CROATIAN_URL = "http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1hr&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0"
LIVE_BOSNIAN_URL = "http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1bih&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0"

"""
FUNCTIONS
"""

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

YOUTUBE_PTN = 'plugin://plugin.video.youtube/play/?video_id=%s'
def youtube_url(videoid):
    return YOUTUBE_PTN % (videoid)

def INDEX():
    add_live_stream(LIVE_SERBIAN_URL, u'N1 Live [Srbija]', 'Program za region Srbije')
    add_live_stream(LIVE_CROATIAN_URL, 'N1 Live [Hrvatska]', 'Program za region Hrvatske')
    add_live_stream(LIVE_BOSNIAN_URL, 'N1 Live [BiH]', 'Program za region BiH')
    
    add_show_folder(PRESSING_SHOW)
    add_show_folder(DNEVNIK_19_SHOW)
    add_show_folder(CRVENA_LINIJA_SHOW)

    xbmcplugin.endOfDirectory(addon_handle)

def add_live_stream(url, title, plot): 
    HEADERS = urllib.urlencode({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'})
    url = url + '|%s' % HEADERS
    li = xbmcgui.ListItem(title, iconImage=iconImage)
    li.setProperty('isplayable', 'true')
    li.setProperty('fanart_image', fanart)
    infoLabels = { 'plot' : plot}
    li.setInfo( type="video", infoLabels=infoLabels)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    

def FOLDER(folder_name, pagetoken = ''):
    if folder_name == None:
        INDEX()
        return

    items = None
    show_fanart = fanart
    iconUrl = iconImage

    show = None

    if folder_name == PRESSING_SHOW.title:
        show = PRESSING_SHOW
    elif folder_name == DNEVNIK_19_SHOW.title:
        show = DNEVNIK_19_SHOW
    elif folder_name == CRVENA_LINIJA_SHOW.title:
        show = CRVENA_LINIJA_SHOW

    if show != None:
        #items = = helper.get_show_data(show.webPage)
        items = helper.get_show_data_yt(show.yt_playlist_id, pagetoken)
        iconUrl = show.iconUrl
        show_fanart = show.fanartUrl
    
    if items == None:
        INDEX()
        return
        
    for item in items:
        if item.title == helper.NEXT_PAGE:
            add_next_prev_folder(folder_name, item.title, item.yt_id, iconUrl, show_fanart)
        else:
            add_show_item(item, fanart = show_fanart)

    xbmcplugin.endOfDirectory(addon_handle)

    
def add_show_item(item, fanart):  
    url = youtube_url(item.yt_id)
    li = xbmcgui.ListItem(item.title, iconImage=item.thumb)
    li.setProperty('isplayable', 'true')
    li.setProperty('fanart_image', fanart)
    infoLabels = {'plot' : item.description}  
    li.setInfo( type="video", infoLabels=infoLabels) 
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

def add_show_folder(show, pagetoken = ''):
    url = build_url({'mode': 'folder', 'foldername':show.title, 'pagetoken':pagetoken})
    li = xbmcgui.ListItem(show.title, iconImage=show.iconUrl)
    li.setProperty('fanart_image', show.fanartUrl)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
   
def add_next_prev_folder(showname, title, pagetoken = '', iconUrl = iconImage, fanartUrl = fanart):
    url = build_url({'mode': 'folder', 'foldername':showname, 'pagetoken':pagetoken})
    li = xbmcgui.ListItem(title, iconImage = iconUrl)
    li.setProperty('fanart_image', fanartUrl)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
                
"""
MAIN
"""

mode = args.get('mode', None)

PRESSING_SHOW = ShowInfo()
PRESSING_SHOW.webPage = 'http://rs.n1info.com/a4557/TV-Emisije/Pressing/Pressing.html'
PRESSING_SHOW.title = "Pressing"
PRESSING_SHOW.fanartUrl = "http://static.rs.n1info.com/Picture/2505/jpeg/presing-700.jpg"
PRESSING_SHOW.iconUrl = iconImage
PRESSING_SHOW.yt_playlist_id = "PLtkTKfgc4b4V87X6A3qLbUGSqnvKNLjLo"

DNEVNIK_19_SHOW = ShowInfo()
DNEVNIK_19_SHOW.webPage = 'http://rs.n1info.com/a4549/TV-Emisije/Dnevnik-u-19/Dnevnik-u-19h.html'
DNEVNIK_19_SHOW.title = "Dnevnik u 19 [Srbija]"
DNEVNIK_19_SHOW.fanartUrl = "http://static.rs.n1info.com/Picture/2494/jpeg/19h.jpg"
DNEVNIK_19_SHOW.iconUrl = iconImage
DNEVNIK_19_SHOW.yt_playlist_id = "PLtkTKfgc4b4VA7ytBRgVS1tHpQ7cC_VoT"

CRVENA_LINIJA_SHOW = ShowInfo()
CRVENA_LINIJA_SHOW.webPage = 'http://rs.n1info.com/a104633/TV-Emisije/Crvena-linija/Crvena-linija.html'
CRVENA_LINIJA_SHOW.title = "Crvena Linija"
CRVENA_LINIJA_SHOW.fanartUrl = 'http://static.rs.n1info.com/Picture/46806/jpeg/Crvena-Linija-mali-poster-tv-emisija.jpg'
CRVENA_LINIJA_SHOW.iconUrl = iconImage
CRVENA_LINIJA_SHOW.yt_playlist_id = "PLtkTKfgc4b4WnU64YTYTsbCrTnyYhrJcD"



if (mode) is None:
    INDEX()
    
elif mode[0] == 'folder':
    foldername = args.get('foldername', None)
    pagetoken = args.get('pagetoken', '')
    print foldername[0]
    FOLDER(foldername[0], pagetoken=pagetoken)
