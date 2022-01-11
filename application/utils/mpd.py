from flask import current_app as app
import mpd

def getCurrentSong() -> dict:
    artist = "Unknown artist"
    album = "Unknown album"
    title = "Unknown title"
    songdate = ""
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
        client.close()
        client.disconnect()
    except Exception as e:
        print(e)

    return dict(artist=artist, title=title, album=album, songdate=songdate)

def getCurrentPlaylist() -> dict:
    queue = []
    try:
        client = mpd.MPDClient()
        client.timeout = 10
        client.idletimeout = None
        client.connect('localhost', 6600)
        idx = client.playlist().index("file: " + client.currentsong()['file'])
        queue = client.playlistinfo()[idx+1:idx+11]
        client.close()
        client.disconnect()
    except Exception as e:
        print(e)
    return dict(data=queue)
