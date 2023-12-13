function deleteFile(name){
    fetch('/delete',{
        method: 'POST',
        body: JSON.stringify({name: name}),
    }).then((_res) =>{
        window.location.href = "/home";
    });
}
