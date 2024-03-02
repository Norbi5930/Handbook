document.getElementById("editFile").addEventListener("change", function(event) {
    let file = event.target.files[0];
    let reader = new FileReader();

    reader.onload = function(event) {
        var img = document.getElementById("editProfilePicture");
        img.src = event.target.result;
    };

    reader.readAsDataURL(file);
});



document.getElementById("deleteImage").addEventListener("click", function() {
    fetch("/api/delete_image", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "http://192.168.1.2:5000/my_profile"
        }
    })
})