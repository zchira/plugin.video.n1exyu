import sys
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

url = 'http://best.str.n1info.com:8080/stream?sp=n1info&channel=n1srb&stream=1mb&b=6&player=m3u8&u=n1info&p=n1Sh4redSecre7iNf0'
li = xbmcgui.ListItem('N1 RS!', iconImage='icon.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)