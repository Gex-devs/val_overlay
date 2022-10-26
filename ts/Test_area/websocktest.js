const WebSocket = require('ws');

let connection = new WebSocket("ws://127.0.0.1:8765");

function main() {
    connection.onopen = function () {
        console.log('Connected!');
        connection.send('ping'); // Send the message 'Ping' to the server
        setTimeout(function() {
            //your code to be executed after 1 second
            connection.send('stop')
          }, 3000);
        
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

