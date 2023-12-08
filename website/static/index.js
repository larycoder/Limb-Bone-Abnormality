function deleteFile(fileId){
    fetch('/delete-file',{
        method: 'POST',
        body: JSON.stringify({fileId: fileId}),
    }).then((_res) =>{
        window.location.href = "/home";
    });
}

function deleteFolder(folderId) {
    fetch('/delete-folder', {
        method: 'POST',
        body: JSON.stringify({ folderId: folderId }),
    }).then((_res) => {
        window.location.href = "/home";
    });
}