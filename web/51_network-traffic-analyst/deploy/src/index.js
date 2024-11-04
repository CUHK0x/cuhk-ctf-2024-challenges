const express = require('express');
const app = express();
const server = require('http').createServer(app);
const WebSocket = require('ws');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const dotenv = require('dotenv').config()

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const wss = new WebSocket.Server({ server });

const messages = [];

const FLAG = process.env.FLAG || "cuhk24ctf{test-flag}";

function heartbeat() {
    this.isAlive = true;
}

function isJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

wss.on('connection', function connection(ws, req) {
    ws.isAlive = true;
    ws.on('error', console.error);
    ws.on('message', function message(data) {
        // handling API
        data = data.toString().replace(/[\r|\n|\t]/g,"")
        console.log(`${ws._socket.remoteAddress}: ${data}`)
        if (isJsonString(data)) {
            const recvData = JSON.parse(data);
            switch (recvData["op"]) {
                case "init":
                    ws.send(JSON.stringify({
                        "op": "flag1",
                        "content": FLAG
                    }));
                    const censoredMessages = messages.map((obj) => {
                        return {
                            "message": obj["message"],
                            "owner": ws._socket.remoteAddress === obj["ip"],
                            "date": obj["date"]
                        }
                    });
                    ws.send(JSON.stringify({
                        "op": "init",
                        "content": censoredMessages
                    }));
                    break;
                case "message":
                    var recvMessage = DOMPurify.sanitize(recvData["content"]).slice(0, 200);
                    if (recvData["content"].length > 200) {
                        recvMessage += "..."
                    }
                    
                    const recvTime = new Date();
                    messages.push({
                        "message": recvMessage, 
                        "ip": ws._socket.remoteAddress,
                        "date": recvTime
                    });
                    if (messages.length >= 100) {
                        messages.splice(0, 50);
                    }
    
                    wss.clients.forEach((client) => {
                        client.send(JSON.stringify({
                            "op": "message",
                            "content": recvMessage,
                            "owner": client._socket.remoteAddress === ws._socket.remoteAddress,
                            "date": recvTime
                        }));
                    });
                    console.log(`Received message ${recvMessage} from ${ws._socket.remoteAddress}`);
                    break;
                default:
                    ws.send(JSON.stringify({
                        "op": "error",
                        "content": "Invalid operation!"
                    }));
                    break;
            }
        } else {
            ws.send(JSON.stringify({
                "op": "error",
                "content": "Invalid JSON!"
            }));
        }
    });
    ws.on('pong', heartbeat);
});
const interval = setInterval(function ping() {
    wss.clients.forEach(function each(ws) {
        if (ws.isAlive === false) return ws.terminate();
        ws.isAlive = false;
        ws.ping();
    });
}, 30000);
wss.on('close', function close() {
    clearInterval(interval);
});

app.use('/', express.static('static'))
server.listen(3000, () => console.log(`Listening on port 3000`))