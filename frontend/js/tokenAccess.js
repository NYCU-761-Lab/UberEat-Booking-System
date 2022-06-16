$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    console.log(accessToken);

    let showAlert = false;
    if (accessToken === null) {  // relocate to the login page
        window.location.replace("index.html");
        showAlert = true;
    } else {
        showAlert = false;
    }

    if (showAlert) {
        alert("Please login!");
    }
});