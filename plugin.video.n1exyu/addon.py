import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

YOUTUBE_PTN = 'plugin://plugin.video.youtube/play/?video_id=%s'
def youtube_url(videoid):
    return YOUTUBE_PTN % (videoid)


mode = args.get('mode', None)

#print "mode"
my_addon = xbmcaddon.Addon("plugin.video.n1exyu")
iconImage = my_addon.getAddonInfo('icon')
fanart = my_addon.getAddonInfo('fanart')

if (mode) is None:
    url = 'http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1srb&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0'
    li = xbmcgui.ListItem('N1 Live [Serbia]', iconImage=iconImage)
    li.setProperty('isplayable', 'true')
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    url = 'http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1hr&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0'
    li = xbmcgui.ListItem('N1 Live [Croatia]', iconImage=iconImage)
    li.setProperty('isplayable', 'true')
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    url = 'http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1bih&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0'
    li = xbmcgui.ListItem('N1 Live [BiH]', iconImage=iconImage)
    li.setProperty('isplayable', 'true')
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    
#    url = build_url({'mode': 'folder', 'foldername':'Pressing'})
#    li = xbmcgui.ListItem('Pressing', iconImage='icon.png')
#    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
#                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

    
elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    url = youtube_url('KSW-L-aZ_OY')
    li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    li.setProperty('isplayable','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
    
