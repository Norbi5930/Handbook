document.addEventListener("DOMContentLoaded", function() {
    var titleInput = document.getElementById("title");
    var descriptionInput = document.getElementById("description");
    var fileInput = document.getElementById("file");

    titleInput.addEventListener("keypress", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            descriptionInput.focus();
        }
    });

    descriptionInput.addEventListener("keypress", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            fileInput.focus();
        }
    });

    fileInput.addEventListener("keypress", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            titleInput.focus();
        }
    });
});



document.getElementById("file").addEventListener("change", function(event) {
    let file = event.target.files[0];   
    let reader = new FileReader();

    reader.onload = function(event) {
        var img = document.getElementById("Img");    
        img.src = event.target.result;
        img.style.display = "block";
    };

    reader.readAsDataURL(file);
});


function scan_post() {
    let titleInput = document.getElementById("title");
    let button = document.getElementById("button");

    if (titleInput.value.length > 0) {
        button.style.display = "block";
    } else {
        button.style.display = "none";
    }
};


setInterval(scan_post, 1000)