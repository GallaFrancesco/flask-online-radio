# Online Radio 
Online radio station built on top of the Icecast server using MPD as the streaming client. It is a server-centric website bridging backend streaming Icecast server with frontend GUI. It is written in Python Flask with websockets (flask_sockets) to provide song information from MPD.

URLs for main homepage:   
http://fragal.eu/webradio

Forked from https://github.com/ExperimentalHypothesis/flask-online-radio to support MPD as a streaming client.

## Requirements

- python3 and pip3
- A running MPD instance (default on `localhost:6600`) with a `shout` endpoint configured
- A running Icecast2 instance to serve the audio stream
- `gunicorn` to serve the Flask application as wsgi and run the websocket worker.
