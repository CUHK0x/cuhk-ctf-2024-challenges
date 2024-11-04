const ws = new WebSocket(`ws://${window.location.host}`);
function heartbeat() {
    clearTimeout(this.pingTimeout);
    this.pingTimeout = setTimeout(() => {
        this.terminate();
    }, 30000 + 1000);
}
// Connection opened
ws.addEventListener("open", (event) => {
    heartbeat()
    const initBlob = {
        "op": "init",
        "content": ""
    };
    ws.send(JSON.stringify(initBlob));
});
var currentMessages = [];
function updateMessages() {
    const content = document.querySelector('#content');
    content.innerHTML = this.currentMessages.map((text) =>
        `
        <div class="col">
            <div class="card mx-auto" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">${text["owner"] ? "You" : "Annonymous"} said:</h5>
                    <p class="card-text"> ${text["message"]} </p>
                </div>
                <div class="card-footer text-body-secondary">
                    ${new Date(text["date"]).toLocaleString()}
                </div>
            </div>
        </div>
        `
    ).reverse().join('');
}
// Listen for messages
ws.addEventListener("message", (event) => {
    const recvData = JSON.parse(event.data);
    switch (recvData["op"]) {
        case "init":
            const allMessages = recvData["content"];
            this.currentMessages = allMessages;
            updateMessages();
            break;
        case "message":
            this.currentMessages.push({"message": recvData["content"], "owner": recvData["owner"], "date": recvData["date"]});
            updateMessages();
            break;
        case "error":
            const errorMessage = recvData["content"];
            alert(errorMessage);
            break;
        default:
            break;
    };
});
ws.addEventListener("ping", heartbeat);
ws.addEventListener("close", function clear() {
    clearTimeout(this.pingTimeout);
});
document.querySelector('#btn').addEventListener('click', () => {
    const messageBlob = {
        "op": "message",
        "content": document.querySelector('#input').value
    };
    ws.send(JSON.stringify(messageBlob));
});