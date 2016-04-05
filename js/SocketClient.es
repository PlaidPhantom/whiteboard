class SocketClient {
    constructor(boardId) {
        this.boardId = boardId;
        this.connection = new WebSocket("ws://localhost:8080/socket/" + boardId);
        this.connection.onopen = this.connect;
    }

    connect() {

    }

    setMessageHandler(handler) {
        this.connection.onmessage = function(event) {
            console.log('Receiving: ' + event.data);
            handler(JSON.parse(event.data));
        };
    }

    sendMessage(message) {
        var msg = JSON.stringify(message);
        console.log('Sending: ' + msg);
        this.connection.send(msg);
    }

    attachMessageReceiver(handler) {
        this.messageReceiver = handler;
    }
}
