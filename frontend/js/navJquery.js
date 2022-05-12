$(document).ready(function() {
    const accessToken = localStorage.getItem("tokenStorage");
    const account = localStorage.getItem("accountStorage");
    let request_url = "http://127.0.0.1:8080";

    // get user's information
    let headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + accessToken
    }
    fetch(request_url + "/auth", {
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
        $("#accountBalance").html(0);
    });

    
    // edit location
    $("#locationBtn").click(function() {
        let new_latitude = $("#editLatitude").val();
        let new_longitude = $("#editLongitude").val();

        // check whether the new value is valid
        if (!(-90 <= new_latitude && new_latitude <= 90)) {
            alert("輸入數值有誤，修改失敗");
        } else if (!(-180 <= new_longitude && new_longitude <= 180)) {
            alert("輸入數值有誤，修改失敗");
        } else if (new_latitude === "" || new_longitude === "") {
            alert("欄位空白，修改失敗");
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

            fetch(request_url + "/auth/location", {
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
                } else if (statusCode === 401) {
                    alert("無法修改此帳戶，修改失敗");
                } else if (statusCode === 400) {
                    alert("輸入數值有誤，修改失敗");
                }
            });
        }
    });
});