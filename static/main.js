function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        // You can use AJAX to send the file to the server
        // For simplicity, let's just display the file name here
        document.getElementById('result').innerHTML = 'File uploaded: ' + file.name;
    } else {
        alert('Please choose a file to upload.');
    }
}