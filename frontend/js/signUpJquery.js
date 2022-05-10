$(document).ready(function() {
    $(".passwordPlace").on("input", function() {
        let password = $("#password").val();
        let re_password = $("#re-password").val();

        if (password === re_password) $("#repasswordText").html("");
        else {
            $("#repasswordText").html("密碼不相符");
            $("#repasswordText").css("color", "red");
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
    $("#accountText").on("input", function() {
        let request_url = "http://127.0.0.1:8080";
        let account = $("#accountText").val();
        // 有長度才會送

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
        let canSignUp = true;

        // 檢查欄位是否空白
        if (name === "" || phone_number === "" || account === "" || password === "" || re_password === "" || latitude === "" || longitude === "") {
            alert("註冊失敗：欄位不能空白");
            canSignUp = false;
        }

        // 檢查密碼驗證是否相符
        if (password != re_password) {
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
                    window.location.replace("index.html");
                } else if (statusCode === 400) {
                    // 欄位空白的情況已經被確認過，只需要確認格式錯誤
                    let errorMsg = myJson['message'];
                    let errorType = errorMsg.split(" ")[1];
                    
                    // 顯示錯誤提示
                    if (errorType === 'username') {
                        $("#nameText").html("輸入格式錯誤");
                        $("#nameText").css("color", "red");
                    } else if (errorType === 'phone') {
                        $("#phonenumberText").html("輸入格式錯誤");
                        $("#phonenumberText").css("color", "red");
                    } else if (errorType === 'account') {
                        $("#accountText").html("輸入格式錯誤");
                        $("#accountText").css("color", "red");
                    } else if (errorType === 'password') {
                        $("#passwordText").html("輸入格式錯誤");
                        $("#passwordText").css("color", "red");
                    } else if (errorType === 'latitude') {
                        $("#latitudeText").html("輸入格式錯誤");
                        $("#latitudeText").css("color", "red");
                    } else if (errorType === 'longitude') {
                        $("#longitudeText").html("輸入格式錯誤");
                        $("#longitudeText").css("color", "red");
                    }
                }
                // console.log(myJson);  // yoona's message
            });
        }


    });
});