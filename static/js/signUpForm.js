function showPassword() {
    var pf = document.getElementById("password");
    var prf = document.getElementById("password_repeat");
    if (pf.type === "password"){
        pf.type = "text";
        prf.type = "text";
    } else {
        pf.type = "password";
        prf.type = "password";
    }
}