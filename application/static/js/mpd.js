var WebsocketClass = function(host){
    this.socket = new WebSocket(host);
}

var interval_id;
var timer_ticks = 0; // every 5 update msg send also a playlist msg
var reconnecting_attempt = false;

WebsocketClass.prototype = {
    initWebsocket : function(){
        var $this = this;
        this.socket.onmessage = function(e){
            $this._onMessageEvent(e);
        };
        this.socket.onclose = function(){
            $this._onCloseEvent();
        };
        this.socket.onopen = function() {
            $this._onOpenEvent();
        }
        this.socket.onerror = function() {
            $this._onCloseEvent();
        }
    },
    sendUpdate : function(){
        var $this = this;
        $this.socket.send('update');
    },
    sendPlaylist : function() {
        var $this = this;
        if (!(timer_ticks % 5)) {
            $this.socket.send('playlist');
            timer_ticks = -1;
        } else {
            timer_ticks += 1;
        }
    },
    initAutoSend : function(){
        var $this = this;
        interval_id = setInterval(
            function(){ $this.sendUpdate(); $this.sendPlaylist(); },
            1000); // update time (1s)
    },
    _onOpenEvent : function() {
        Messenger().post({
            message: 'Connected to Server.',
            type: 'success'
        });
    },
    _onMessageEvent : function(e){
        var parsed = JSON.parse(e.data);
        if (parsed['received'] == 'update') {
            document.getElementById("artist").innerHTML = parsed['artist'];
            document.getElementById("album").innerHTML = parsed['album'];
            document.getElementById("title").innerHTML = parsed['title'];
            if(parsed['songdate'] === "") {
                document.getElementById("songdate").innerHTML = "";
            } else {
                document.getElementById("songdate").innerHTML = parsed['title'];
            }
        }
        else if(parsed['received'] == 'playlist') {
            var data = parsed['data'];
            var ul = document.getElementById("playlist-ul");
            while(ul.firstChild){
                ul.removeChild(ul.firstChild);
            }
            for(var i=0; i<data.length; i++) {
                var obj = data[i];
                var li = document.createElement("li");
                var small = document.createElement("small");
                small.className = "playlist-txt"
                small.appendChild(document.createTextNode(obj.artist + " - " + obj.title))
                li.appendChild(small);
                ul.appendChild(li);
            }
        }
        else {
            Messenger().post({
                message: parsed['received'],
                type: 'success'
            });
        }
    },
    _onCloseEvent : function(){
        window.clearInterval(interval_id)
        if(reconnecting_attempt == false) {
            reconnecting_attempt = true;
            var connect = 0;
            window.clearInterval(interval_id);
            console.log("y is it disconnected?")
            Messenger().run({
                errorMessage: 'Disconnected from Server',
                action: function(opts) {
                    if(connect == 0) {
                        connect = 1;
                        return opts.error({
                            status: 1000,
                            readyState: 0,
                            responseText: 0
                        });
                    }
                    ws = new WebsocketClass("wss://fragal.eu/webradio/_socket_mpd");
                    ws.initWebsocket();
                    ws.initAutoSend();
                    reconnecting_attempt = false;
                    return opts.success();
                }
            });
        }
    }
};

// Initialize a new websocket (the first one)
var ws = new WebsocketClass("wss://fragal.eu/webradio/_socket_mpd");
window.setTimeout('ws.initWebsocket()', 1000);
ws.initAutoSend();

// Before changing the page, we close the socket correctly.
window.onbeforeunload = function() {
    ws.socket.onclose = function () {};
    ws.socket.close()
};
