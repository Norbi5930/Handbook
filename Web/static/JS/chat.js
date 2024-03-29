const input = document.getElementById("input");
const button = document.getElementById("button");


window.addEventListener("DOMContentLoaded", function() {
    let chatContainer = document.getElementById("container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
});

input.addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        sendMessage();
    };
});

button.addEventListener("click", function() {
    sendMessage();
});




function sendMessage() {
    let message = input.value;
    console.log(window.location.href)
    if (message.length > 0 && message.length < 200) {
       fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            }
        )
       })
       .then(response => response.json())
       .then(data => {
            if (data.success) {
                window.location.reload()
            }
       })
       .catch(error => {
            console.error("Error: ", error)
       })
    } else {}
}


