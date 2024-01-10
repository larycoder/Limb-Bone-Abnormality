function deleteUser(customerId){
    fetch('/delete-user',{
        method: 'POST',
        body: JSON.stringify({userId: customerId}),
    }).then((_res) =>{
	    window.locatin.href="/admin";
        window.location.reload();
    });
}
