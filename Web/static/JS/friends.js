



function removeFriend(friendID) {
    fetch("/api/friend/remove", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            friendID: friendID
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload()
        } else {
            alert("A művelet nem sikerült! Próbáld újra később!")
        }
    })
    .catch(error => {
        console.error("Error: ", error)
    })
}