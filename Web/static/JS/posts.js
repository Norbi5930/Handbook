function reportPost(postID) {
    fetch("/api/report_post", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            postID: postID
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload()
        }
    })
}


function deletePost(postID, code) {
    let reportMessage = document.getElementById("reportMessage");
    fetch("/posts/" + postID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            code: code,
            reportMessage: reportMessage.value
        })
    })
    .then(response => response.json())
    .then(data => {})
}