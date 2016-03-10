class SocketClient {
    constructor(boardId) {
        this.boardId = boardId;
        this.connection = new WebSocket("ws://localhost:8080/boards/" + boardId);
        this.connection.onopen(this.connect);
    }

    function setMessageHandler(handler) {
        this.connection.onmessage = function(event) {
            handler(JSON.parse(event.data));
        };
    }

    function sendMessage(msg) {
        this.connection.send(JSON.stringify(msg));
    }

    function attachMessageReceiver(handler) {
        this.messageReceiver = handler;
    }
}
