document.getElementById("togglePassword").onclick=(event)=>{
  const passwordInput=document.getElementById("password");
  const toggleButton=document.getElementById("togglePassword");
  event.preventDefault()
  if(passwordInput.type === "password"){
    passwordInput.type = "text";
    toggleButton.textContent = "Hide";
  } 
  else{
    passwordInput.type = "password";
    toggleButton.textContent = "Show";
  }
}
