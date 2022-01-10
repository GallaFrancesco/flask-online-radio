from flask import current_app as app
import mpd

def parseSong(client, sinfo):
    song = client.currentsong()
    if 'title' in song:
        sinfo['title'] = song['title']
    if 'artist' in song:
        sinfo['artist'] = song['artist']
    if 'album' in song:
        sinfo['album'] = song['album']
    if 'date' in song:
        sinfo['songdate'] = song['date']
    return sinfo 

def getCurrentSong(client) -> dict:
    sinfo = dict()
    sinfo['artist'] = "Unknown artist"
    sinfo['album'] = "Unknown album"
    sinfo['title'] = "Unknown title"
    sinfo['songdate'] = ""
    try: 
        return parseSong(client, sinfo)
    except ConnectionError as e: # connect again
        client = mpd.MPDClient()
        client.timeout = 10
        client.idletimeout = None
        client.connect('localhost', 6600)
        return parseSong(client, sinfo)
    except Exception as e:
        print(e)
        return sinfo 

