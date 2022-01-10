# -*- coding: utf-8 -*-
import json
import mpd

from application import sockets
from .utils.mpd import getCurrentSong

@sockets.route('/_socket_mpd')
def socket_mpd(ws):
    while True:
        message = ws.receive()
        if message == "update":
            song = getCurrentSong()
            artist = song['artist'];
            album = song['album'];
            title = song['title'];
            songdate = song['songdate'];
            ws.send(json.dumps(dict(received=message, artist=artist, album=album, title=title, songdate=songdate)))
        else:
            ws.send(json.dumps(dict(received=message)))
