const WebSocket = require('ws');

let connection = new WebSocket("ws://192.168.1.13:4444");

function main() {
    

    connection.onopen = function () {
        console.log('Connected!');
        connection.send('Ping'); // Send the message 'Ping' to the server
    };

    // Log errors
    connection.onerror = function (error) {
        console.log('WebSocket Error ' + error.error);
    };

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data);
    };

}

main();

