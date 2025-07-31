function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function create_patient() {
    const given_name = document.querySelector("#given-name").value;
    const family_name = document.querySelector("#family-name").value;

    return fetch("/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            resourceType: "Patient",
            name: [
                {
                    use: "official",
                    given: [given_name],
                    family: family_name
                }
            ]
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#new-patient").onsubmit = function (event) {
        event.preventDefault();
        create_patient();
    }
});