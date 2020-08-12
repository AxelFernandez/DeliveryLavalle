  $(document).ready(function() {
        $("#id_photo").attr('accept', 'image/x-png,image/jpeg');

  })
function previewFile() {

    var preview = document.querySelector('img');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        var FileSize = file.size / 1024 / 1024; // in MB
        if (FileSize > 1) {
            preview.src = "";
            $("#warning-image").show()


        }else{
            reader.readAsDataURL(file);
        }
    } else {
        preview.src = "";
    }
}

