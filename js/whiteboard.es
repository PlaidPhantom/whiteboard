(function($) {

    const idle = Symbol('idle');
    const drawing = Symbol('drawing');

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
            this.timeout = setTimeout(() => {
                this.state = idle;
                this.timeout = null;
            }, 2000);
        },
        killTimeout: function() {
            clearTimeout(this.timeout);
            this.timeout = null;
        }
    };

    function getEventPoint(event) {
        var x = event.offsetX;
        var y = event.offsetY;

        return x + ',' + y;
    }

    drawingState.board._.events({
        mousedown: function(event) {
            switch(drawingState.state) {
                case idle:
                    drawingState.state = drawing;
                    drawingState.newPath('M' + getEventPoint(event));
                    break;
                case drawing:
                    drawingState.append('M' + getEventPoint(event));
                    drawingState.killTimeout();
                    break;
                default:
                    console.log('bad drawing state! ' + drawingState.state);
            }
        },
        mousemove: function(event) {
            if(drawingState.state === drawing) {
                drawingState.append('L' + getEventPoint(event));
            }
        },
        'mouseup mouseout': function(event) {
            drawingState.startTimeout();
        }
    });


})($);
