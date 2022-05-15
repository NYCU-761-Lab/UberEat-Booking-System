$(document).ready(function() {
    const accessToken = localStorage.getItem("tokenStorage");
    const account = localStorage.getItem("accountStorage");
    let request_url = "http://127.0.0.1:8080";

    // when clicking the shop menu page:
    // 1. show the shop information
    // 2. cannot modify the shop's info if the shop has been created
    $("#shopItem").click(async function() {
        let statusCode = null;
        let shopName = null;
        
        // Get shop's name. If shop name exists, disable the input place.
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // Get the shop information with shop name.
        if (shopName != null) {
            let shopCategory = null;
            let shopLatitude = null;
            let shopLongitude = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            let body = {
                'shop_name': shopName,
            }

            // shop category
            shopCategory = await fetch(request_url + "/shop/get_shop_type", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    return myJson['shop_type of the shop_name'];
                }
            });
            // shop latitude
            shopLatitude = await fetch(request_url + "/shop/get_shop_latitude", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    return myJson['latitude of the shop_name'];
                }
            });
            // shop longitude
            shopLongitude = await fetch(request_url + "/shop/get_shop_longitude", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    return myJson['longitude of the shop_name'];
                }
            });

            $('.registerShopName').attr('placeholder', shopName);
            $('.registerShopCategory').attr('placeholder', shopCategory);
            $('.registerShopLatitude').attr('placeholder', shopLatitude);
            $('.registerShopLongitude').attr('placeholder', shopLongitude);

            $('.registerShopName').attr('disabled','disabled');
            $('.registerShopCategory').attr('disabled','disabled');
            $('.registerShopLatitude').attr('disabled','disabled');
            $('.registerShopLongitude').attr('disabled','disabled');
            $('#shopRegisterBtn').attr('disabled','disabled');
        }
    });

    // check whether the shop name has been used
    $(".registerShopName").on("input", function() {
        let shopName = $('.registerShopName').val();
        if (shopName != "") {
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            let body = {
                'shop_name': shopName,
            }

            fetch(request_url + "/shop/check_name", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    $("#shopNameText").html("");
                } else if (statusCode === 400) {
                    $("#shopNameText").html(myJson['message']);
                    $("#shopNameText").css("color", "red");
                } else if (statusCode === 409) {
                    $("#shopNameText").html(myJson['message']);
                    $("#shopNameText").css("color", "red");
                }
            });
        }
    });

    // register shop
    $('#shopRegisterBtn').click(function() {
        let shopName = $('.registerShopName').val();
        let shopCategory = $('.registerShopCategory').val();
        let shopLatitude = $('.registerShopLatitude').val();
        let shopLongitude = $('.registerShopLatitude').val();

        if (shopName === "" || shopCategory === "" || shopLatitude === "" || shopLongitude === "") {
            alert("The field cannot be left blank.");
        } else {
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'shop_name': shopName,
                'shop_type': shopCategory,
                'latitude': shopLatitude,
                'longitude': shopLongitude
            }

            let statusCode = null;
            fetch(request_url + "/shop/register", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    alert(myJson['message']);
                    location.reload();  // refresh the page
                } else {
                    alert(myJson['message']);
                }
            });
        }
    });
});