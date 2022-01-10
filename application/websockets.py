# -*- coding: utf-8 -*-
import json
import mpd

from application import sockets
from .utils.mpd import getCurrentSong

client = mpd.MPDClient()
client.timeout = 10
client.idletimeout = None
client.connect('localhost', 6600)

@sockets.route('/_socket_mpd')
def socket_mpd(ws):
    while True:
        message = ws.receive()
        if message == "update":
            song = getCurrentSong(client)
            artist = song['artist'];
            album = song['album'];
            title = song['title'];
            songdate = song['songdate'];
            ws.send(json.dumps(dict(received=message, artist=artist, album=album, title=title, songdate=songdate)))
        else:
            ws.send(json.dumps(dict(received=message)))
