httpProxy = require('http-proxy');

var options = {
    pathnameOnly: true,
    router: {
        '/': '127.0.0.1:8081',
        '/socket': '127.0.0.1:8082'
    }
};

httpProxy.createServer(options).listen(8080);
