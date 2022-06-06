$(document).ready(function() {
    const accessToken = localStorage.getItem("tokenStorage");
    const account = localStorage.getItem("accountStorage");
    let request_url = "http://127.0.0.1:8080";

    // log out
    $(".logOutBtn").click(function() {
        window.location.replace("index.html");
        localStorage.removeItem("tokenStorage");
        localStorage.removeItem("accountStorage");
    });


    // get user's information
    let headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + accessToken
    }
    fetch(request_url + "/auth/get_account_info", {
        method: 'POST',
        headers: headers,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        $("#accountAccount").html(myJson['account']);
        $("#accountName").html(myJson['username']);
        $("#accountRole").html(myJson['role']);
        $("#accountPhone").html(myJson['phone_number']);
        $("#accountLatitude").html(myJson['latitude']);
        $("#accountLongitude").html(myJson['longitude']);
        $("#accountBalance").html(myJson['balance']); 
    });

    
    // edit location
    $("#locationBtn").click(function() {
        let new_latitude = $("#editLatitude").val();
        let new_longitude = $("#editLongitude").val();

        // check whether the new value is valid
        if (new_latitude === "" || new_longitude === "") {
            alert("The fields cannot be left blank.");
        } else {
            // edit database
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'latitude': new_latitude,
                'longitude': new_longitude
            }

            fetch(request_url + "/auth/edit_location", {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    $("#accountLatitude").html(new_latitude);
                    $("#accountLongitude").html(new_longitude);
                    alert(myJson['message']);
                } else {
                    alert(myJson['message']);
                }
            });
        }
    });
});