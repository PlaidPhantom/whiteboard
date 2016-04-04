var http = require('http')
var httpProxy = require('http-proxy');

var wsProxy = httpProxy.createProxyServer({ ws: true, target: 'ws://localhost:8082/' });
var httpProxy = httpProxy.createProxyServer({ target: 'http://localhost:8081/' });

var server = http.createServer(function(req, res) {
  httpProxy.web(req, res);
});

server.on('upgrade', function (req, socket, head) {
  wsProxy.ws(req, socket, head);
});

server.listen(8080);
