const editButton = document.getElementById("profileEdit");
const aboutMe = document.getElementById("aboutMe");

let edit = false;
let textarea;

editButton.addEventListener("click", function() {
    if (edit) {
        edit = false;
        textarea.parentNode.replaceChild(aboutMe, textarea);
        if (confirm("Biztosan megszeretnéd változtatni?")) {
            aboutMe.innerHTML = textarea.value;
            editAbout(textarea.value);
        }
    } else {
        edit = true;
        textarea = document.createElement("textarea");
        textarea.placeholder = aboutMe.innerHTML;
        aboutMe.parentNode.replaceChild(textarea, aboutMe);
        textarea.classList.add("profile-edit");
    }
});



function editAbout(content) {
    fetch("/api/edit_about", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            window.location.reload();
        }
    });
};

document.getElementById("profilePicture").addEventListener("click", function() {
    window.location.href = "http://192.168.1.4:5000/my_profile/edit";
});


const settingsButton = document.getElementById("setttingsChangeButton");

settingsButton.addEventListener("click", function() {
    const settingsEmail = document.getElementById("settingsEmail");

    if (settingsEmail.value.indexOf("@") !== -1 && settingsEmail.value.indexOf(".") !== -1) {
        fetch("/api/change_email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: settingsEmail.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload()
            } else {
                if (data.errorMessage) {
                    alert(data.errorMessage)
                } else {
                    alert("A művelet nem sikerült! Próbáld újra később!")   
                };
            };
        })
        .catch(error => {
            console.error("Error: ", error)
        })
    } else {
        alert("Nem megfelelő formátum!")
    }
})
