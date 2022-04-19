document.querySelector('#welcome-message .sending-time').innerHTML = formatDate(new Date());

const messageTextBox = document.getElementById("text-input");
const chatWindow = document.getElementById("chat-window");
const sentimentValue = document.getElementById("sentiment-value");
const BOT_NAME = "stoky_bot";
const PERSON_NAME = "You";

document.getElementById("input-form")
.addEventListener("submit", event => {
    event.preventDefault();
    if (!messageTextBox.value) return;
    appendMessage(PERSON_NAME, "sent", messageTextBox.value);
    botResponse(messageTextBox.value);
    messageTextBox.value = "";
});

function appendMessage(name, side, text) {
    const messageHTML = `
<div class="message ${side}-message">
    <div class="message-bubble">
        <div class="message-header">
            <div class="sender-name">${name}</div>
            <div class="sending-time">${formatDate(new Date())}</div>
        </div>
        <div class="message-text">${text}</div>
    </div>
</div>
`;
    chatWindow.insertAdjacentHTML("beforeend", messageHTML);
    chatWindow.scrollTop += 500;
}

function appendBotMessage(name, side, text, sentiment) {
    const messageHTML = `
<div class="message ${side}-message">
    <div class="message-bubble">
        <div class="message-header">
            <div class="sender-name">${name}</div>
            <div class="message-sentiment">Sentiment Value: ${sentiment}</div>
            <div class="sending-time">${formatDate(new Date())}</div>
        </div>
        <div class="message-text">${text}</div>
    </div>
</div>
`;
    chatWindow.insertAdjacentHTML("beforeend", messageHTML);
    chatWindow.scrollTop += 500;
}

function botResponse(rawText) {
    $.get("/get", { message: rawText }).done(function (data) {
    let output = data.split("<septoken>")
    appendBotMessage(BOT_NAME, "received", output[0], output[1] - 3);
    updateSentiment(output[1]);
    });
}

function updateSentiment(value) {
    sentimentValue.innerText = (parseInt(sentimentValue.textContent) + parseInt(value) - 3).toString()
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}