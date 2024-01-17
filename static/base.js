function checkURL(){
    let arr=['ourstory', 'pipeline', 'demo','login','sign-up','admin','add_user','home']
    var currentURL=window.location.href;
    url=currentURL.split("/")
    url_now=url[url.length-1]
    arr.forEach((value) => {
        if(value===url_now){
            let btn=document.getElementById(value);
            btn.classList.add("energetic")
        }
        else{
            let btn=document.getElementById(value);
            if(btn!=null){
                btn.classList.remove("energetic")
            }
        }
    });
}

document.getElementById("icon").onclick=(event)=>{
    const passwordInput=document.getElementById("password");
    const toggleButton=document.getElementById("icon");
    event.preventDefault()
    if(passwordInput.type === "password"){
        passwordInput.type = "text";
        toggleButton.src="../static/images/eye-close.png";
    } 
    else{
        passwordInput.type = "password";
        toggleButton.src="../static/images/eye-show.png";
    }
}

document.getElementById("re-icon").onclick=(event)=>{
    const passwordInput=document.getElementById("re-password");
    const toggleButton=document.getElementById("re-icon");
    event.preventDefault()
    if(passwordInput.type === "password"){
        passwordInput.type = "text";
        toggleButton.src="../static/images/eye-close.png";
    } 
    else{
        passwordInput.type = "password";
        toggleButton.src="../static/images/eye-show.png";
    }
}