function verifyWholeForm()  {
    var x = 0;
    if((document.getElementById("nameMsg") === null)&&(document.getElementById("surnameMsg") === null)&&(document.getElementById("usernameMsg") === null)&&(document.getElementById("passwordMsg") === null)&&(document.getElementById("photoMsg") === null)
    &&(document.getElementById("name").value !== "")&&(document.getElementById("surname").value !== "")&&(document.getElementById("username").value !== "")&&(document.getElementById("password").value !== "")&&(document.getElementById("passwordRepeat").value !== "")&&(document.getElementById("img").value !== "")){
        document.getElementById("submitBtn").disabled = false;
    }   else    {
        document.getElementById("submitBtn").disabled = true;
    }
}

function checkIfNameOk() {
    var list = document.getElementById("signUpList");
    if(document.getElementById("name").value.length<2){
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Name must be atleast 2 characters long!");
        entry.appendChild(entryText);
        entry.id ="nameMsg";
        list.insertBefore(entry,document.getElementById("nameLI"));
        verifyWholeForm();
    }   else if(/\s{2,}/.test(document.getElementById("name").value) == true) {

        var entry = document.createElement("li");
        var entryText = document.createTextNode("Name can't have more than 2 whitespaces in a row!");
        entry.appendChild(entryText);
        entry.id ="nameMsg";
        list.insertBefore(entry,document.getElementById("nameLI"));
        verifyWholeForm();

    }   
}


function deleteNameMsg() {
    var list = document.getElementById("signUpList");
    var tmp = document.getElementById("nameMsg");
    if(tmp != null) {
        list.removeChild(tmp);
        verifyWholeForm();
    }
}


function checkIfSurnameOk() {
    var list = document.getElementById("signUpList");
    if(document.getElementById("surname").value.length<3){
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname must be atleast 3 characters long!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));
        verifyWholeForm();
    }   else if(/\s{2,}/.test(document.getElementById("surname").value) == true) {

        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname can't have more than 2 whitespaces in a row!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));
        verifyWholeForm();

    }   
}


function deleteSurnameMsg() {
    var list = document.getElementById("signUpList");
    var tmp = document.getElementById("surnameMsg");
    if(tmp != null) {
        list.removeChild(tmp);
        verifyWholeForm();
    }
}


function deleteUsernameMsg(){

}

function checkIfUsernameOk(){
    
}








function checkIfPasswordOk() {
    var list = document.getElementById("signUpList");
    if(document.getElementById("password").value.length<8){
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password must be atleast 8 characters long!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
        verifyWholeForm();
    
    }   else if(/\s+/.test(document.getElementById("password").value) == true) {

        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password can't have any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
        verifyWholeForm();

    }   else if(document.getElementById("password").value !== document.getElementById("passwordRepeat").value){
    
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password must be same!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
        verifyWholeForm();
    }
}


function deletePasswordMsg() {
    var list = document.getElementById("signUpList");
    var tmp = document.getElementById("passwordMsg");
    if(tmp != null) {
        list.removeChild(tmp);
        verifyWholeForm();
    }
}

function showPassword() {
    var pf = document.getElementById("password");
    var prf = document.getElementById("passwordRepeat");
    if (pf.type === "password"){
        pf.type = "text";
        prf.type = "text";
    } else {
        pf.type = "password";
        prf.type = "password";
    }
}

