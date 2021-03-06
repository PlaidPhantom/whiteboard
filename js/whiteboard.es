(function($) {

    const idle = Symbol('idle');
    const drawing = Symbol('drawing');
    const waiting = Symbol('waiting');

    const drawingState = {
        server: null,
        board: $('#board'),
        state: idle, // 'idle', 'drawing'
        timeout: null,
        curPath: null,
        pathString: '',
        prevPathIds: [],
        pathId: null,
        append: function(data) {
            console.log(data);
            this.pathString += data;
            this.curPath.setAttribute('d', this.pathString);
            this.send(data);
        },
        newPath: function(id) {
            console.log('new path id: ' + id);
            this.pathString = '';
            this.prevPathIds.push(this.pathId);
            this.pathId = id;
            this.curPath = document.createElementNS("http://www.w3.org/2000/svg", 'path');
            this.curPath.setAttribute('id', id);
            this.curPath.setAttribute('d', this.pathString);
            this.board.appendChild(drawingState.curPath);
        },
        startTimeout: function() {
            this.state = waiting;
            this.timeout = setTimeout(() => {
                this.state = idle;
                this.timeout = null;
                this.server.sendMessage({ type: 'fin-path' });
            }, 2000);
        },
        killTimeout: function() {
            this.state = drawing;
            clearTimeout(this.timeout);
            this.timeout = null;
        },

        sendBuffer: '',
        sendTimeout: null,
        send: function(data) {
            if(this.sendTimeout)
                clearTimeout(this.sendTimeout);

            this.sendBuffer += data;

            this.sendTimeout = setTimeout(() => {
                var data = this.sendBuffer;
                this.sendBuffer = '';
                this.sendTimeout = null;

                this.server.sendMessage({
                    type: 'add-path',
                    id: this.pathId,
                    data: data
                })
            }, 500);
        }
    };

    drawingState.server = new SocketClient(drawingState.board.getAttribute('data-boardid'))

    drawingState.server.setMessageHandler(function(message) {
        switch(message.type) {
            case 'need-auth':
                var pass = prompt('Enter Passphrase');
                drawingState.server.sendMessage({ type: 'auth', passphrase: pass });
                break;
            case 'cur-state':
                for(var path of message.paths) {
                    var element = document.createElementNS("http://www.w3.org/2000/svg", 'path');
                    element.setAttribute("id", path.id);
                    element.setAttribute('d', path.data);
                    drawingState.board.appendChild(element);
                }
                break;
            case 'path-id':
                drawingState.newPath(message.id);
                break;
            case 'add-path':
                if(message.id != drawingState.pathId && !drawingState.prevPathIds.some(p => p === message.id)) {
                    path = drawingState.board.getElementById(message.id);
                    if(path)
                        path.d += message.data;
                    else {
                        var element = document.createElementNS("http://www.w3.org/2000/svg", 'path');
                        element.setAttribute("id", message.id);
                        element.setAttribute('d', message.data);
                        drawingState.board.appendChild(element);
                    }
                }
                break;
            default:
                alert('Error: Unknown message type');
        }
    });

    function getEventPoint(event) {
        var x = event.offsetX;
        var y = event.offsetY;

        return x + ',' + y;
    }

    function startedDrawing(event) {
        if(event.target !== this)
            return;
        console.log(event);
        switch(drawingState.state) {
            case idle:
                drawingState.state = drawing;
                drawingState.append('M' + getEventPoint(event));
                break;
            case waiting:
                drawingState.killTimeout();
                drawingState.append('M' + getEventPoint(event));
                break;
            default:
                console.log('bad drawing state! ' + drawingState.state);
        }

        return false;
    }

    function keptDrawing(event) {
        if(event.target !== this)
            return;
        if(drawingState.state === drawing) {
            drawingState.append('L' + getEventPoint(event));
        }
        return false;
    }

    function stoppedDrawing(event) {
        console.log(event);
        drawingState.startTimeout();
        return false;
    }

    drawingState.board.addEventListener('mousedown', startedDrawing, true);
    drawingState.board.addEventListener('mousemove', keptDrawing, true);
    drawingState.board.addEventListener('mouseup', stoppedDrawing, true);
    //drawingState.board.addEventListener('mouseout', stoppedDrawing, true);


})($);
