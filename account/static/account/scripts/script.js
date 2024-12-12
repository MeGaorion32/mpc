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
    

    $('#delete-user-avatar').on('click', function() {
        let update = $(this).data('update');
        let csrfToken = '';
        let user_id = ''

        console.log('update', update);
        console.log('update type', typeof update);

        if (update == 'True') {
            csrfToken = $(this).data('token');
            user_id = $(this).data('id');

            console.log('token', csrfToken);
            console.log('user_id', user_id);

            $.ajax({
                url: '/user/delete/avatar/' + user_id + '/',  // URL вашего представления
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken // Передаем CSRF-токен в заголовках
                },
                processData: false,
                contentType: false,
                success: function(response) {               
                   
                    alert('Файлы успешно удален!');  // Успешное сообщение                
                    // location.reload();
                },
    
                error: function(xhr, status, error) {
                    console.error(error);
                    alert('Произошла ошибка при удалении.');  // Сообщение об ошибке
                }
    
            });
        }              
        
        $('#register-avatar').val(''); // сбросить значение input file
        $('.avatar-preview-block').empty(); // удалить превью
    });


    $('#change-user').on('click', function() {
        const form = document.getElementById('user-edit-form');
        const formData = new FormData(form);           

        csrfToken = $(this).data('token');
        user_id = $(this).data('id');
        type = $(this).data('type');

        console.log('token', csrfToken);
        console.log('user_id', user_id);

        $.ajax({
            url: '/user/update/' + type + '/' + user_id + '/',  // URL вашего представления
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken // Передаем CSRF-токен в заголовках
            },
            processData: false,
            contentType: false,
            success: function(response) {    
                
                console.log('response', response);                
               
                alert('Пользователь успешно изменен');  // Успешное сообщение                
                location.reload();
            },

            error: function(xhr, status, error) {
                console.error(error);
                alert('Произошла ошибка при изменении пользователя.');  // Сообщение об ошибке
            }

        });

       
    });



})