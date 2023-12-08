function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('file', file);
        document.getElementById('result').innerHTML = 'File uploaded: ' + file.name;
    } else {
        alert('Please choose a file to upload.');
    }
}