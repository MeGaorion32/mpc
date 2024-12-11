$(document).ready(function() {
    $(`#avatar-button`).on('click', function() {
        event.preventDefault(); // чтобы форма не отправлялась при нажатии кнопки        
        $(`#register-avatar`).click();
    });

    $(`#register-avatar`).on('change', function() {
        const files = this.files;    
        if (files && files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('.avatar-preview-block').html(`<img src="${e.target.result}" alt="Preview" class="avatar-preview-image">`);
            }
            reader.readAsDataURL(files[0]);
        }        
      
    });

    $('.btn-danger').on('click', function() {
        $('#register-avatar').val(''); // сбросить значение input file
        $('.avatar-preview-block').empty(); // удалить превью
    });



})