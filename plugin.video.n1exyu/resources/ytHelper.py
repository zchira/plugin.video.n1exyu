import os
import urllib
from apiclient.discovery import build


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
API_KEY = 'AIzaSyAQuy8nvX0nIEZfIwPnzWFfIfath8GRXCM'

#Grabs the videos from a playlist by playlistId
# Params:
    # id: The id of the playlist which videos you want to retrieve
    #nextpage: The nextpage token. Default: false. If set it will retrieve the page. That allows all videos to be parsed, instead of the 50 limit
def vids_by_playlist(id, nextpage = False):
    youtube = build(
      YOUTUBE_API_SERVICE_NAME,
      YOUTUBE_API_VERSION,
      developerKey=API_KEY
    )
    
    if nextpage == False:
        search_response = youtube.playlistItems().list(
          part="snippet,contentDetails",
          maxResults=20,
          playlistId=id
        ).execute()
    else:
        search_response = youtube.playlistItems().list(
          part="snippet,contentDetails",
          maxResults=20,
          playlistId=id,
          pageToken=nextpage
        ).execute()
    
    return search_response
    
