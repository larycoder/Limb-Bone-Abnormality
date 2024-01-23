function deleteF(Id){
    fetch('/delete',{
        method: 'POST',
        body: JSON.stringify({Id: Id}),
    }).then((_res) =>{
        window.location.href = "/home";
    });
}
function deleteSubFile(Id, folder_id){
    fetch('/delete-subfile',{
        method: 'POST',
        body: JSON.stringify({Id: Id}),
    }).then((_res) =>{
        window.location.href = "/folder/"+ folder_id;
    });

}
function deleteFolder(Id) {
    fetch('/delete-folder', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    })
    .then((res) => {
        if (res.ok) {
            return res.json();
        } else {
            throw new Error('Error deleting folder');
        }
    })
    .then((_data) => {
        window.location.href = "/home";
    })
    .catch((error) => {
        console.error(error);
    });
}

function deleteSubFolder(Id, parent_folder_id) {
    fetch('/delete-folder', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    })
    .then((res) => {
        if (res.ok) {
            return res.json();
        } else {
            throw new Error('Error deleting folder');
        }
    })
    .then((_data) => {
        window.location.href = "/folder/"+ parent_folder_id;
    })
    .catch((error) => {
        console.error(error);
    });
}
function changeColor(){
    let step2 = document.getElementById('step-2')
    step2.src = "../static/images/step2_color.png"
}
function executeF(Id){
    changeColor()
    fetch('/execute',{
        method: 'POST',
        body: JSON.stringify({Id: Id}),
    }).then((response) =>{
        if(!response.ok){
            throw new Error("HTTP error! Status:",response.status);
        }
        return response.json();
    }).then(data=>{
        window.location.href="/folder/"+ Id;})
    }



function executeSubF(Id,folder_id){
    fetch('/executeSubF',{
        method: 'POST',
        body: JSON.stringify({Id: Id}),
    }).then((_res) =>{
        window.location.href = "/folder/"+ folder_id;
    });
}