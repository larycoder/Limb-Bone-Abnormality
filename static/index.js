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
function executeF(Id) {
    fetch('/execute', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error! Status:", response.status);
            }
            return response.json();
        })
        .then(data => {
            checkForUpdates(Id);
        })
        .catch(error => console.error('Error executing:', error));
}
executeF(Id);
function checkForUpdates(Id) {
    fetch(`/check_updates/${Id}`)
        .then(response => response.json())
        .then(data => {
            if (data.updated) {
                // If an update is detected, reload the page
                location.reload();
            }
        })
        .catch(error => console.error('Error checking for updates:', error));
}
  // Check for updates every 5 seconds 
setInterval(() => checkForUpdates(Id), 5000);

function executeSubF(Id,folder_id){
    fetch('/executeSubF',{
        method: 'POST',
        body: JSON.stringify({Id: Id}),
    }).then((_res) =>{
        window.location.href = "/folder/"+ folder_id;
    });
}