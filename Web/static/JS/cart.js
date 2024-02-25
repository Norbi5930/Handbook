




function remove_cart(itemID) {
    console.log(itemID)
    fetch("api/remove_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            itemID: itemID
        })
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
}