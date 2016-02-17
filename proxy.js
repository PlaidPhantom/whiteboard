var SimpleReverseProxy = require('simple-reverse-proxy'),
    SimplePathRouter = require('simple-path-router');

new SimplePathRouter()
    .when('/', new SimpleReverseProxy(['http://localhost:8081']))
    .when('/socket', new SimpleReverseProxy(['http://localhost:8082']))
    .listen(8080);
