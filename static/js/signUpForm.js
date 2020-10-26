function verifyWholeForm()  {
    var x = 0;
    if((document.getElementById("nameMsg") === null)&&(document.getElementById("surnameMsg") === null)&&(document.getElementById("usernameMsg") === null)&&(document.getElementById("passwordMsg") === null)&&(document.getElementById("photoMsg") === null)
    &&(document.getElementById("name").value !== "")&&(document.getElementById("surname").value !== "")&&(document.getElementById("username").value !== "")&&(document.getElementById("password").value !== "")&&(document.getElementById("passwordRepeat").value !== "")&&(document.getElementById("img").value !== "")&&((document.getElementById("Male").checked)||(document.getElementById("Female").checked))){
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
        verifyWholeForm();
    }   else if(/\s{2,}/.test(document.getElementById("name").value) == true) {

        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Name can't have more than 2 whitespaces in a row!");
        entry.appendChild(entryText);
        entry.id ="nameMsg";
        list.insertBefore(entry,document.getElementById("nameLI"));
        verifyWholeForm();

    }   
}


function deleteNameMsg() {
    var tmp = document.getElementById("nameMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
        verifyWholeForm();
    }
}


function checkIfSurnameOk() {
    if(document.getElementById("surname").value.length<3){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname must be atleast 3 characters long!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));
        verifyWholeForm();
    }   else if(/\s{2,}/.test(document.getElementById("surname").value) == true) {
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Surname can't have more than 2 whitespaces in a row!");
        entry.appendChild(entryText);
        entry.id ="surnameMsg";
        list.insertBefore(entry,document.getElementById("surnameLI"));
        verifyWholeForm();

    }
}


function deleteSurnameMsg() {
    var tmp = document.getElementById("surnameMsg");
    if(tmp != null) {
        var list = document.getElementById("signUpList");
        list.removeChild(tmp);
        verifyWholeForm();
    }
}


function checkIfUsernameOk(){
    if(document.getElementById("username").value.length<8){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Username must be atleast 8 characters long!");
        entry.appendChild(entryText);
        entry.id ="usernameMsg";
        list.insertBefore(entry,document.getElementById("usernameLI"));
        verifyWholeForm();
    }   else if(/\s/.test(document.getElementById("username").value) == true) {
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Username can't have any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="usernameMsg";
        list.insertBefore(entry,document.getElementById("usernameLI"));
        verifyWholeForm();
    }   else {
        var xhr = new XMLHttpRequest();
        var url = "https://infinite-hamlet-29399.herokuapp.com/check/" + document.getElementById("username").value;
        
        xhr.open('GET',url);
        xhr.onreadystatechange = function(){
            var DONE = 4;
            var OK = 200;
            if(xhr.readyState == DONE){
                if(xhr.status == OK){
                    console.log(xhr.responseText);
                    msg = xhr.responseText;

                    var list = document.getElementById("signUpList");
                    var entry = document.createElement("li");
                    var entryText = document.createTextNode(xhr.responseText);
                    entry.appendChild(entryText);
                    entry.id ="usernameMsg";
                    list.insertBefore(entry,document.getElementById("usernameLI"));
                    verifyWholeForm();
                } else {
                    console.log('Error: ' + xhr.status);
                }
            }
        }
        xhr.send(null);

    }
}



function deleteUsernameMsg(){
    var tmp = document.getElementById("usernameMsg");
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
        verifyWholeForm();
    
    }   else if(/\s+/.test(document.getElementById("password").value) == true) {

        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password can't have any whitespaces!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
        verifyWholeForm();

    }   else if(document.getElementById("password").value !== document.getElementById("passwordRepeat").value){
        var list = document.getElementById("signUpList");
        var entry = document.createElement("li");
        var entryText = document.createTextNode("Password must be same!");
        entry.appendChild(entryText);
        entry.id ="passwordMsg";
        list.insertBefore(entry,document.getElementById("passwordLI"));
        verifyWholeForm();
    }
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

