
const navPing = document.getElementById("navPing")
window.addEventListener("DOMContentLoaded", function() {
    this.setInterval(get_notifications, 100000);
})


function get_notifications() {
    fetch("/api/get_notifications", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.notifications) {
                let notifications = data.notifications;
                let ping = 0;
                
                notifications.forEach(notification => {
                    if (!notification.read) {
                        ping++;
                    };
                });
                if (ping > 0) {
                    navPing.style.display = "block";
                    navPing.textContent = ping;
                }
            };
        } 
    })
    .catch(error => {
        console.error("Error: ", error);
    });
}