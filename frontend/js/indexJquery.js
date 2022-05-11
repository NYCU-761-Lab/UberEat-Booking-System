$(document).ready(function() {
    $(".signInBtn").click(function() {
       let account = $("#Account").val();
       let password = $("#password").val();
       let request_url = "http://127.0.0.1:8080";
       
       // checking
       if (account === "" || password === "") {
           alert("登入失敗");
       } else {
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            let body = {
                'account': account,
                'password': password,
            }

            fetch(request_url + "/auth/login", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if(statusCode === 200) {
                    const accessToken = myJson['access_token'];
                    localStorage.setItem("tokenStorage", accessToken);
                    localStorage.setItem("accountStorage", account);
                    window.location.replace("nav.html");
                }
                else alert("登入失敗");
            })
        }
    });
});