


function acceptFriendRequest(requestID) {
    fetch("/api/friend_request/accept", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            requestID: requestID
        })
    })
    .then(respose => respose.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Sikertelen művelet! Kérlek próbáld újra később!")
        }
    })
    .catch(error => {
        console.error("Error: ", error)
    })
};


function rejectFriendRequest(requestID) {
    fetch("/api/friend_request/reject", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            requestID: requestID
        })
    })
    .then(respose => respose.json())
    .then(data => {
        if (data.success) {
            window.location.reload()
        } else {
            alert("Sikertelen művelet! Kérlek próbáld újra később!")
        }
    })
}
