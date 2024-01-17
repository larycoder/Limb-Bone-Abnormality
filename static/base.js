function checkURL(){
    let arr=['ourstory', 'pipeline', 'demo','login','sign-up','admin','add_user']
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