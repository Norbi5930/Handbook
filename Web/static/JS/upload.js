

document.getElementById("file").addEventListener("change", function(event) {
    let file = event.target.files[0];   
    let reader = new FileReader();

    reader.onload = function(event) {
        var img = document.getElementById("previewImg");    
        img.src = event.target.result;
        img.style.display = "block";
    };

    reader.readAsDataURL(file);
})