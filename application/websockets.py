# -*- coding: utf-8 -*-
import json
import mpd

from application import sockets
from .utils.mpd import getCurrentSong, updatePlaylist

@sockets.route('/_socket_mpd')
def socket_mpd(ws):
    queue = []
    while True:
        message = ws.receive()
        if message == "update":
            song = getCurrentSong()
            song['received'] = message
            ws.send(json.dumps(song))
        elif message == "playlist":
            queue = updatePlaylist(queue)
            ws.send(json.dumps(dict(received=message, data=queue)))
        else:
            ws.send(json.dumps(dict(received=message)))
        
