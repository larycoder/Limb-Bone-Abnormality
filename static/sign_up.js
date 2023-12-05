function valid(){
    let password=document.getElementById('password').value
    let re_password=document.getElementById('re-password').value
    // let username=document.getElementById('username').value
    if(validPass(password, re_password)){
        if(checkUser()){
            alert("Account created successfully")
            window.location.href='/sign_in'
        }
        else{
            alert("Username already exists")
        }
    }
    else{
        alert("Password and re-password does not match")
    }
}

function checkUser(){
    fetch(`register`)
    .then(response=>{
        if(!response.ok){
            throw new console.error('Network response is not ok')
        }
        return response.json()
    })
    .then(data=>{
        console.log(`data: ${data}`)
    })
    .catch(error=>{
        console.error(`Catch error: ${error}`)
    })
}

function validPass(password, re_password){
    return password===re_password
}