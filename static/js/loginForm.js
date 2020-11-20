function verifyForm()  {
    if((document.getElementById("username").value !== "")&&(document.getElementById("password").value !== ""))
    {
        document.getElementById("signInBtn").disabled = false;
    }   else    {
        document.getElementById("signInBtn").disabled = true;
    }
}

document.getElementById("username").addEventListener("blur",function() { verifyForm()});
document.getElementById("password").addEventListener("blur",function() { verifyForm()});
