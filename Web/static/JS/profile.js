const requestButton = document.getElementById("requestButton");



function friendRequest(userID) {
    fetch("/api/friend_request", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            userID: userID
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            requestButton.textContent = "Elküldve!";
        } else {
            if (data.errorMessage) {
                alert(data.errorMessage)
            } else {
                alert("A művelet nem sikerült! Kérlek próbáld újra később!")
            }
        }
    })
}