
function verifyWholeForm()  {
    if((document.getElementById("nameMsg") === null)&&(document.getElementById("surnameMsg") === null)&&(document.getElementById("usernameMsg") === null)&&(document.getElementById("passwordMsg") === null)&&(document.getElementById("emailMsg") === null)&&(document.getElementById("addressMsg") === null)&&
    (document.getElementById("name").value !== "")&&(document.getElementById("surname").value !== "")&&(document.getElementById("username").value !== "")&&(document.getElementById("password").value !== "")&&(document.getElementById("passwordRepeat").value !== "")&&(document.getElementById("email").value !== "")&&(document.getElementById("address").value !== ""))
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


function checkIfUsernameOk(){
    
    if(/^[a-z]{3,12}$/.test(document.getElementById("username").value) == false) {
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Username must be between 3 and 12 lowercase letters!");
        entry.appendChild(entryText);
        entry.id ="usernameMsg";
        list.insertBefore(entry,document.getElementById("usernameLI"));
    }   else {
        var xhr = new XMLHttpRequest();
        var username = document.getElementById("username").value;
        var url = "https://infinite-hamlet-29399.herokuapp.com/check/" + username;
            
        fetch(url).then(function(response) {
            if(response.status !== 200) {
                console.log("Problem occured. Status code : " + response.status);
                return;
            }   else{
                return response.json();
            }
        }).then(function(json){
            var loginStatus = json[username];
            if(loginStatus==="taken"){
                var list = document.getElementById("signUpList");
                var entry = document.createElement("li");
                var entryText = document.createTextNode("Username is already taken!");
                entry.appendChild(entryText);
                entry.id ="usernameMsg";
                list.insertBefore(entry,document.getElementById("usernameLI"));
            }
            console.log(loginStatus);

        }).catch(function(error){
            console.log('Error: '+ error);
        });
    }
    verifyWholeForm();
}



function deleteUsernameMsg(){
    var tmp = document.getElementById("usernameMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
    }
    verifyWholeForm();
}


function checkIfEmailOk() {
    if(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(document.getElementById("email").value) == false) {
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Email is incorrect!");
        entry.appendChild(entryText);
        entry.id ="emailMsg";
        list.insertBefore(entry,document.getElementById("emailLI"));
    }   
    verifyWholeForm();
}

function deleteEmailMsg() {
    var tmp = document.getElementById("emailMsg");
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


function checkIfPasswordOk() {
    if(document.getElementById("password").value.length<8){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password must be atleast 8 characters long!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
    
    }   else if(/\s+/.test(document.getElementById("password").value) == true) {

        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password can't have any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));

    }   else if(document.getElementById("password").value !== document.getElementById("passwordRepeat").value){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password must be same!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
    }
    verifyWholeForm()
}


function deletePasswordMsg() {
    var tmp = document.getElementById("passwordMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
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

document.getElementById("name").addEventListener("focus",function() {   deleteNameMsg() });
document.getElementById("name").addEventListener("blur",function() {    checkIfNameOk() });

document.getElementById("surname").addEventListener("focus",function() { deleteSurnameMsg()});
document.getElementById("surname").addEventListener("blur",function() { checkIfSurnameOk()});

document.getElementById("username").addEventListener("focus",function() { deleteUsernameMsg()});
document.getElementById("username").addEventListener("blur",function() { checkIfUsernameOk()});

document.getElementById("email").addEventListener("focus",function() { deleteEmailMsg()});
document.getElementById("email").addEventListener("blur",function() { checkIfEmailOk()});

document.getElementById("address").addEventListener("focus",function() { deleteAddressMsg()});
document.getElementById("address").addEventListener("blur",function() { checkIfAddressOk()});

document.getElementById("password").addEventListener("focus",function() { deletePasswordMsg()});
document.getElementById("password").addEventListener("blur",function() { checkIfPasswordOk()});

document.getElementById("passwordRepeat").addEventListener("focus",function() { deletePasswordMsg()});
document.getElementById("passwordRepeat").addEventListener("blur",function() { checkIfPasswordOk()});

document.getElementById("showPasswordBtn").addEventListener("change",function() { showPassword()});
