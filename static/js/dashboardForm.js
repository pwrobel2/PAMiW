function verifyForm()  {
    if((document.getElementById("name").value !== "")&&(document.getElementById("lockerID").value !== "")&&(document.getElementById("size").value !== ""))
    {
        document.getElementById("submitBtn").disabled = false;
    }   else    {
        document.getElementById("submitBtn").disabled = true;
    }
}

document.getElementById("name").addEventListener("blur",function() { verifyForm()});
document.getElementById("lockerID").addEventListener("blur",function() { verifyForm()});
document.getElementById("size").addEventListener("blur",function() { verifyForm()});
