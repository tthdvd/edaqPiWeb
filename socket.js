var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var Redis = require('ioredis');
var redis = new Redis(6379, 'localhost', {password: 'alma123'});
var pub = new Redis(6379, 'localhost', {password: 'alma123'});

redis.subscribe('edaq530', function(err, count) {
});
redis.on('message', function(channel, message) {
    console.log('Message Recieved: ' + message);
    msg = JSON.parse(message);
    io.emit(msg.event, msg.data);
});

io.on('connection', function (socket) {
    socket.on("mesurement_status", function (msg) {
        send_data = {'event': 'mesurement_status', 'data': msg};
        pub.publish('edaq530', JSON.stringify(send_data))
    });

    socket.on("schedule_task", function (msg) {
        send_data = {'event': 'schedule_task', 'data': msg};
        pub.publish('edaq530', JSON.stringify(send_data))
    });

    socket.on('ask_active_threads', function (msg) {
        send_data = {'event': 'ask_active_threads'};
        pub.publish('edaq530', JSON.stringify(send_data))
    })
});

http.listen(6002, function(){
    console.log('Listening on Port 6002');
});
