
const token = '' + Math.random();
var ip_address;

fetch("https://ipinfo.io/ip")
.then(res => res.text())
.then(data => ip_address = data);

const fetchMessage = () => {
    fetch("http://localhost:8080/messages?token=" + token)
    .then(res => res.json())
    .then(data => {updateMessage(data); fetchMessage()});
}

const updateMessage = (messages) => {
    const messageElement = document.getElementsByClassName("message")[0];
    document.getElementById("content").innerHTML = "";
    for(const message of messages){
        const new_message = messageElement.cloneNode(true);
        new_message.getElementsByClassName("author")[0].innerHTML = message["author"];
        new_message.getElementsByClassName("body")[0].innerHTML = message["body"];
        document.getElementById("content").appendChild(new_message);
    }
}
fetchMessage();


const submit = () => {
    const param = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            author: ip_address,
            body: document.getElementById("submitText").value
        })
    };
    fetch("http://localhost:8080/post", param)
    .then(document.getElementById("submitText").value = "");
}