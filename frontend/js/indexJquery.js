$(document).ready(function() {
    $(".signInBtn").click(function() {
       let account = $("#Account").val();
       let password = $("#password").val();
       let request_url = "http://127.0.0.1:8080";
       
       // checking
       if (account === "" || password === "") {
           alert("登入失敗");
       } else {
           $.ajax({
               url: request_url + "/auth/login",
               method: "POST",
               dataType: "json",
               data: {
                   'account': account,
                   'password': password,
               },
               success: function(data) {
                   console.log(data);
                   if (data === 200) { 
                       window.location.replace("nav.html");
                   } else {
                       alert("登入失敗");
                   }
               }
           });
            // window.location.replace("nav.html");
        }
    });
});