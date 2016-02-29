(function($) {

    const idle = Symbol('idle');
    const drawing = Symbol('drawing');
    const waiting = Symbol('waiting');

    const drawingState = {
        board: $('#board'),
        state: idle, // 'idle', 'drawing'
        timeout: null,
        curPath: null,
        pathString: '',
        append: function(data) {
            console.log(data);
            this.pathString += data;
            this.curPath.setAttribute('d', this.pathString);
        },
        newPath: function(data) {
            console.log(data);
            this.pathString = data;
            this.curPath = document.createElementNS("http://www.w3.org/2000/svg", 'path');
            this.curPath.setAttribute('d', this.pathString);
            this.board.appendChild(drawingState.curPath);
        },
        startTimeout: function() {
            this.state = waiting;
            this.timeout = setTimeout(() => {
                this.state = idle;
                this.timeout = null;
            }, 2000);
        },
        killTimeout: function() {
            this.state = drawing;
            clearTimeout(this.timeout);
            this.timeout = null;
        }
    };

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
                drawingState.newPath('M' + getEventPoint(event));
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
