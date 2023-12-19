function updateFile(id){
    data=document.getElementById("data").innerHTML
    fetch(`/file/${id}/updateFile`,{
        method: 'POST',
        body: JSON.stringify({data: data}),
    }).then((_res) =>{
        window.location.href = `/file/${id}`;
    });
}