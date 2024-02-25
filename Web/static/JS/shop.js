




function addCart(itemID) {
    fetch("api/add_cart", {
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
            alert("Sikeresen hozzáadva a kosarához!");
        } else {
            if (data.errorcode == 315) {
                window.location.href = "http://127.0.0.1:5000/login"
            }
        }
    })
}