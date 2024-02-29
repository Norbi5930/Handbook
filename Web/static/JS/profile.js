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
            edit_about(textarea.value);
        }
    } else {
        edit = true;
        textarea = document.createElement("textarea");
        textarea.placeholder = aboutMe.innerHTML;
        aboutMe.parentNode.replaceChild(textarea, aboutMe);
        textarea.classList.add("profile-edit");
    }
});



function edit_about(content) {
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
    })
}