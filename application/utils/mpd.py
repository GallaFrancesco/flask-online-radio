from flask import current_app as app
import mpd

def getCurrentSong() -> dict:
    artist = "Unknown artist"
    album = "Unknown album"
    title = "Unknown title"
    songdate = "n/a"
    missing = "n/a"
    try: # connect / disconnect each time (and monitor)
        client = mpd.MPDClient()
        client.timeout = 10
        client.idletimeout = None
        client.connect('localhost', 6600)
        song = client.currentsong()
        if 'title' in song:
            title = song['title']
        if 'artist' in song:
            artist = song['artist']
        if 'album' in song:
            album = song['album']
        if 'date' in song:
            songdate = song['date']
        status = client.status()
        missing = int(float(status['duration']) - float(status['elapsed']))
        client.close()
        client.disconnect()
    except Exception as e:
        print(e)
    return dict(artist=artist, title=title, album=album, songdate=songdate, missing=missing)

def getCurrentPlaylist(client = None, idx = 0) -> list:
    queue = []
    try:
        if not client:
            client = mpd.MPDClient()
            client.timeout = 10
            client.idletimeout = None
            client.connect('localhost', 6600)
        queue = client.playlistinfo()[idx+1:idx+11]
        client.close()
        client.disconnect()
    except Exception as e:
        print(e)
    return queue

def updatePlaylist(queue = [], client = None) -> list:
    try:
        if not client:
            client = mpd.MPDClient()
            client.timeout = 10
            client.idletimeout = None
            client.connect('localhost', 6600)
        status = client.status()
        idx = int(status['song'])
        elapsed = float(status['elapsed'])
        if elapsed < 5 or not queue: # song started from less than 5 seconds or queue empty
            queue = getCurrentPlaylist(client, idx)
        else:
            client.close()
            client.disconnect()
    except Exception as e:
        print(e)
    return queue
