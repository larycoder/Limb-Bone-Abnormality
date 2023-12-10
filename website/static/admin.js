function deleteUser(customerId){
    fetch('/delete-user',{
        method: 'POST',
        body: JSON.stringify({userId: customerId}),
    }).then((_res) =>{
        window.location.href = "/admin";
    });
}