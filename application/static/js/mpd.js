var WebsocketClass = function(host){
    this.socket = new WebSocket(host);
}

var current_interval_id;
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
    initAutoSend : function(){
        var $this = this;
        current_interval_id = setInterval(
            function(){ $this.socket.send('update'); },
            500) // update time
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
            $(".artist").text(parsed['artist']);
            $(".album").text(parsed['album']);
            $(".title").text(parsed['title']);
            $(".songdate").text(parsed['songdate']);
        }
        else {
            Messenger().post({
                message: parsed['received'],
                type: 'success'
            });
        }
    },
    _onCloseEvent : function(){
        window.clearInterval(current_interval_id)
        if(reconnecting_attempt == false) {
            reconnecting_attempt = true;
            var connect = 0;
            window.clearInterval(current_interval_id);
            Messenger().run({
                errorMessage: 'Disconnected from Server',
                action: function(opts) {
                    if(connect == 0) {
                        connect = 1;
                        return opts.error({
                            status: 500,
                            readyState: 0,
                            responseText: 0
                        });
                    }
                    ws = new WebsocketClass("ws://fragal.eu/webradio/_socket_mpd");
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
var ws = new WebsocketClass("ws://fragal.eu/webradio/_socket_mpd");
window.setTimeout('ws.initWebsocket()', 500);
ws.initAutoSend();

// Before changing the page, we close the socket correctly.
window.onbeforeunload = function() {
    ws.socket.onclose = function () {};
    ws.socket.close()
};
