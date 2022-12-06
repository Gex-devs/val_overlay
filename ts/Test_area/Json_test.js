const WebSocket = require('ws');
const discovery = require('discovery');

// Create a WebSocket server on port 8080
const wss = new WebSocket.Server({ port: 8080 });

// Advertise the WebSocket server on the local network
discovery.advertiser.start('my-websocket-server', 8080);

// When a client connects to the server, log a message
wss.on('connection', (ws) => {
  console.log('A client connected to the server');
});
