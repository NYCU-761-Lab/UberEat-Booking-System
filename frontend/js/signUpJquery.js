$(document).ready(function() {
    $(".passwordPlace").on("input", function() {
        let password = $("#password").val();
        let re_password = $("#re-password").val();

        if (password === re_password) $("#passwordText").html("");
        else {
            $("#passwordText").html("密碼不相符");
            $("#passwordText").css("color", "red");
        }
    });
  
    $(".signUpBtn").click(function() {
        let name = $("#name").val();
        let phone_number = $("#phonenumber").val();
        let account = $("#Account").val();
        let password = $("#password").val();
        let re_password = $("#re-password").val();
        let latitude = $("#latitude").val();
        let longitude = $("#longitudee").val();

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
            $.ajax({
                url: request_url + "/auth/register",
                method: "POST",
                dataType: "json",
                data: {
                    'name': name,
                    'phone_number': phone_number,
                    'account': account,
                    'password': password,
                    'latitude': latitude,
                    'longtitude': longtitude
                },
                success: function(data) {
                    console.log(data);
                    if (data === 200) { 
                        // window.location.replace("nav.html");
                    } else if (data === 409) {
                        $("#accountText").html("帳號已被使用");
                        $("#accountText").css("color", "red");
                    } else if (data === 422) {
                        alert("註冊失敗：輸入格式不符");
                    } else {
                        console.log(data);
                    }
                }
            });
        }


    });
});