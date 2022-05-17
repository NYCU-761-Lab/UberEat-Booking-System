$(document).ready(function() {
    let canSignUp = true;
    let passwordOK = false;

    $(".passwordPlace").on("input", function() {
        let password = $("#password").val();
        let re_password = $("#re-password").val();

        if (password === re_password) {
            $("#repasswordText").html("");
            passwordOK = true;
            canSignUp = true;
        }
        else {
            $("#repasswordText").html("Password is incorrect.");
            $("#repasswordText").css("color", "red");
            passwordOK = false;
        }
    });

    // 如果有輸入格式錯誤，會有警告提示。因此需要先初始化警告提示
    $("#name").on("input", function() {
        $("#nameText").html("");
    });
    $("#phonenumber").on("input", function() {
        $("#phonenumberText").html("");
    });
    $("#Account").on("input", function() {
        $("#accountText").html("");
    });
    $("#password").on("input", function() {
        $("#passwordText").html("");
    });
    $("#latitude").on("input", function() {
        $("#latitudeText").html("");
    });
    $("#longitude").on("input", function() {
        $("#longitudeText").html("");
    });

    // 檢查 account 是否被使用過
    $(".accountPlace").on("input", function() {
        let request_url = "http://127.0.0.1:8080";
        let account = $(".accountPlace").val();

        if (account != "") {
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            let body = {
                'account': account
            }

            fetch(request_url + "/auth/check_account", {
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
                    $("#accountText").html("");
                    canSignUp = true;
                } else if (statusCode === 400) {
                    $("#accountText").html(myJson['message']);
                    $("#accountText").css("color", "red");
                    canSignUp = false;
                } else if (statusCode === 409) {
                    $("#accountText").html(myJson['message']);
                    $("#accountText").css("color", "red");
                    canSignUp = false;
                }
            });
        }
    });
  
    $(".signUpBtn").click(function() {
        let name = $("#name").val();
        let phone_number = $("#phonenumber").val();
        let account = $("#Account").val();
        let password = $("#password").val();
        let re_password = $("#re-password").val();
        let latitude = $("#latitude").val();
        let longitude = $("#longitude").val();

        let request_url = "http://127.0.0.1:8080";

        // 檢查欄位是否空白
        if (name === "" || phone_number === "" || account === "" || password === "" || re_password === "" || latitude === "" || longitude === "") {
            alert("The fields cannot be blank.");
            canSignUp = false;
        }

        if (passwordOK === false) {
            canSignUp = false;
        }
        
        if (canSignUp) {
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            let body = {
                'username': name,
                'phone_number': phone_number,
                'account': account,
                'password': password,
                'latitude': latitude,
                'longitude': longitude
            }

            let statusCode = null;
            fetch(request_url + "/auth/register", {
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
                    alert("Sign up successfully.");
                    window.location.replace("index.html");
                } else if (statusCode === 400) {
                    // 欄位空白的情況已經被確認過，只需要確認格式錯誤
                    let errorMsg = myJson['message'];
                    let errorType = errorMsg.split(" ")[1];
                    
                    // 顯示錯誤提示
                    if (errorType === 'username') {
                        $("#nameText").html(myJson['message']);
                        $("#nameText").css("color", "red");
                    } else if (errorType === 'phone') {
                        $("#phonenumberText").html(myJson['message']);
                        $("#phonenumberText").css("color", "red");
                    } else if (errorType === 'account') {
                        $("#accountText").html(myJson['message']);
                        $("#accountText").css("color", "red");
                    } else if (errorType === 'password') {
                        $("#passwordText").html(myJson['message']);
                        $("#passwordText").css("color", "red");
                    } else if (errorType === 'latitude') {
                        $("#latitudeText").html(myJson['message']);
                        $("#latitudeText").css("color", "red");
                    } else if (errorType === 'longitude') {
                        $("#longitudeText").html(myJson['message']);
                        $("#longitudeText").css("color", "red");
                    }
                }
            });
        }
    });
});