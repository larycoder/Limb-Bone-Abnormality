function deleteUser(customerId){
    fetch('/delete-user',{
        method: 'POST',
        body: JSON.stringify({userId: customerId}),
    }).then((_res) =>{
	    window.locatin.href="/admin";
        window.location.reload();
    });
}

// document.getElementById("togglePassword").onclick=()=>{
//   const passwordInput=document.getElementById("password");
//   const toggleButton=document.getElementById("togglePassword");
//   if(passwordInput.type === "password"){
//     passwordInput.type = "text";
//     toggleButton.textContent = "Hide";
//   } 
//   else{
//     passwordInput.type = "password";
//     toggleButton.textContent = "Show";
//   }
// }