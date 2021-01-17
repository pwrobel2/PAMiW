
function verifyWholeForm()  {
    if((document.getElementById("nameMsg") === null)&&(document.getElementById("surnameMsg") === null)&&(document.getElementById("addressMsg") === null)&&
    (document.getElementById("name").value !== "")&&(document.getElementById("surname").value !== "")&&(document.getElementById("address").value !== ""))
    {
        document.getElementById("submitBtn").disabled = false;
    }   else    {
        document.getElementById("submitBtn").disabled = true;
    }
}

function checkIfNameOk() {
    if(document.getElementById("name").value.length<2){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Name must be atleast 2 characters long!");
        entry.appendChild(entryText);
        entry.id ="nameMsg";
        list.insertBefore(entry,document.getElementById("nameLI"));
    }   else if(/^[A-ZĄĆĘŁŃÓŚŻŹ][a-ząćęłńóśżź]+$/.test(document.getElementById("name").value) == false) {

        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Name should start with capital letter and not contain any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="nameMsg";
        list.insertBefore(entry,document.getElementById("nameLI"));
    }
    verifyWholeForm();
}


function deleteNameMsg() {
    var tmp = document.getElementById("nameMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
    }
    verifyWholeForm();
}


function checkIfSurnameOk() {
    if(document.getElementById("surname").value.length<3){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname must be atleast 3 characters long!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));

    }   else if(/^[A-ZĄĆĘŁŃÓŚŻŹ][a-ząćęłńóśżź]+$/.test(document.getElementById("surname").value) == false) {
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname should start with capital letter and not contain any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));
    }
    verifyWholeForm();
}


function deleteSurnameMsg() {
    var tmp = document.getElementById("surnameMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
    }
    verifyWholeForm();
}


function checkIfAddressOk() {
    if(document.getElementById("address").value.length<5){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Address must be atleast 5 characters long!");
        entry.appendChild(entryText);
        entry.id ="addressMsg";
        list.insertBefore(entry,document.getElementById("addressLI"));
    }
    verifyWholeForm();
}


function deleteAddressMsg() {
    var tmp = document.getElementById("addressMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
        verifyWholeForm();
    }
}



document.getElementById("name").addEventListener("focus",function() {   deleteNameMsg() });
document.getElementById("name").addEventListener("blur",function() {    checkIfNameOk() });

document.getElementById("surname").addEventListener("focus",function() { deleteSurnameMsg()});
document.getElementById("surname").addEventListener("blur",function() { checkIfSurnameOk()});

document.getElementById("address").addEventListener("focus",function() { deleteAddressMsg()});
document.getElementById("address").addEventListener("blur",function() { checkIfAddressOk()});
