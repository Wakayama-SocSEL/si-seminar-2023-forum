"use strict";

const token = '' + Math.random();

// メッセージを取得し続ける
// 新しいメッセージがあるまでサーバは返答を待機する
const fetchMessage = () => {
    fetch("http://localhost:8080/messages?token=" + token)
    .then(res => res.json())
    .then(data => {updateMessages(data); fetchMessage()});
}

// メッセージを描画する
const updateMessages = (messages) => {
    const messageElement = document.getElementsByClassName("message")[0];
    document.getElementById("content").innerHTML = "";
    for(const message of messages){
        const new_messageElement = messageElement.cloneNode(true);
        new_messageElement.getElementsByClassName("player-id")[0].innerHTML = message["player_id"];
        new_messageElement.getElementsByClassName("body")[0].innerHTML = message["body"];
        new_messageElement.getElementsByClassName("ng")[0].innerHTML = message["ng"];
        new_messageElement.getElementsByClassName("judge")[0].innerHTML = message["judge"];
        document.getElementById("content").appendChild(new_messageElement);
    }
}

const submit = () => {
    const param = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            token: token,
            body: document.getElementById("submitText").value
        })
    };
    fetch("http://localhost:8080/post", param)
    .then(document.getElementById("submitText").value = "");
}

fetchMessage();
