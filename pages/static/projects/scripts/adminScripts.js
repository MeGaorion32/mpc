$(document).ready(function() {     

    fieldsList.forEach((field, index) => {
        $(`#${field.buttonId}`).on('click', function() {
            $(`#${field.inputId}`).click();
        });

        $(`#${field.inputId}`).on('change', function() {
            const files = this.files;            
            // for (let i = 0; i < files.length; i++) {
            //     // console.log('filesList 1', filesList);
            //     // console.log('index', index);
                
            //     filesList[index].files.push(files[i]);
            //     const fileURL = URL.createObjectURL(files[i]);
            //     // $(`#${field.ulId}`).append(`<li>${files[i].name}</li>`);  // Отображаем имена файлов
            //     $(`#files-list-block-${index+1}`).append(`
            //         <img id="files-list-image-${index+1}-${i+1}" 
            //         class="files-list-image" src="${fileURL}" 
            //         alt="${files[i].name}" 
            //         onclick="selectFile(${index}, ${filesList[index].files.length - 1}, '${fileURL}')">
            //         `)
            // }
            setFiles(index, files)
            this.value = '';  // Сброс поля input после выбора
            // console.log('filesList 2', filesList);           
        });
    })   
   

    $('#save-button').on('click', function() {
        let csrfToken = $(this).data('token');
        const form = document.getElementById('project-create-form');
        const formData = new FormData(form);    
        console.log('csrfToken', csrfToken);
        console.log('updatePage form', updatePage);
        formData.append('updatePage', updatePage);
        if(updatePage) {
            formData.append('projectId', projectId);
        }

        filesList.forEach(file => {
            for (let i = 0; i < file.files.length; i++) {
                if(file.name == 'photo' && file.files.length) {
                    formData.append('projectFile', file.files[0]);
                }
                formData.append(file.name, file.files[i]);  // добавляем поле "photos"
                
            }

        })     
        
        console.log('formData', formData);

        $.ajax({
            url: '/projects/create/',  // URL вашего представления
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken // Передаем CSRF-токен в заголовках
            },
            processData: false,
            contentType: false,
            success: function(response) {               
                fieldsList.forEach(field => {
                    $(`#${field.ulId}`).empty();  // Очищаем списки файлов после успешной загрузки
                })
              
                filesList.forEach(file => {
                   file.files = [];        
                })     

                let projectNameInput = $('#project-name-input');
                let projectInfoInput = $('#project-info-text');
                projectNameInput.val('');
                projectInfoInput.val('');
                alert('Файлы успешно загружены!');  // Успешное сообщение                
                // location.reload();
            },

            error: function(xhr, status, error) {
                console.error(error);
                alert('Произошла ошибка при загрузке файлов.');  // Сообщение об ошибке
            }

        });

    });


    $('#remove-file-button').on('click', function() {
        const { fieldIndex, fileIndex, fileId } = selectedFileInfo;
        console.log('fileId', fileId);        

        if (fileId != null) {
            $.ajax({
                url: '/projects/projectFile/delete/' + fileId,  // URL вашего представления
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken // Передаем CSRF-токен в заголовках
                },
                processData: false,
                contentType: false,
                success: function(response) {               
                    
                    alert('Файл успешно удален');  // Успешное сообщение                
                    // location.reload();
                },
    
                error: function(xhr, status, error) {
                    console.error(error);
                    alert('Произошла ошибка при загрузке файлов.');  // Сообщение об ошибке
                }
    
            });

        }

        if (fieldIndex !== null && fileIndex !== null) {
            // Удаляем файл из массива
            filesList[fieldIndex].files.splice(fileIndex, 1);
    
            // Обновляем интерфейс
            $('#selected-file').empty(); // Очищаем блок выбранного файла
            selectedFileInfo = { fieldIndex: null, fileIndex: null }; // Сбрасываем информацию о выбранном файле
    
            // Обновляем список файлов, если нужно
            $(`#files-list-block-${fieldIndex + 1}`).empty(); // Очищаем блок с изображениями
            filesList[fieldIndex].files.forEach((file, i) => {
                const fileURL = URL.createObjectURL(file);
                $(`#files-list-block-${fieldIndex + 1}`).append(`
                    <img id="files-list-image-${fieldIndex + 1}-${i + 1}" 
                    class="files-list-image" src="${fileURL}" 
                    alt="${file.name}" 
                    onclick="selectFile(${fieldIndex}, ${i}, '${fileURL}')">
                `);
            });
        }
    });
    

})

let selectedFileInfo = {
    fieldIndex: null,
    fileIndex: null,
    fileId: null,
};


function selectFile(fieldIndex, fileIndex, fileURL=null, fileId=null) {
    console.log('Select file', fileURL);
    console.log('fileId', fileId);
    console.log('viewerUrl', viewerUrl+'#');
    const extension = fileURL.split('.').pop().split(/[\?#]/)[0]; // получаем часть после последней точки.   

    console.log('File extension:', extension);

    let selectedImage = '';

    // Очищаем предыдущие изображения в блоке
    $('#selected-file').empty();
    // Создаём новый элемент img с переданным URL и добавляем его в блок 
    if(extension == 'pdf') {
        selectedImage = ` <iframe src="${viewerUrl}#${fileURL}" style="width:70%; height:90%;" frameborder="0"></iframe>`;
    } else if (extension == 'mp4' || extension == 'webm') {
        selectedImage = `
        <video class="photo-video-item" style="width:70%; height:90%;" controls>            
            <source src="${fileURL}" type="video/${extension}">
            Your browser does not support the video tag.
        </video>`
    } else {
        selectedImage = `<img class="selected-image" src="${fileURL}" alt="Selected file" class="selected-image">`;
    }    
     
    $('#selected-file').append(selectedImage);

    // Сохраняем информацию о выбранном файле
    selectedFileInfo.fieldIndex = fieldIndex;
    selectedFileInfo.fileIndex = fileIndex;
    selectedFileInfo.fileId = fileId;

}


function setFiles(index, files) {
    for (let i = 0; i < files.length; i++) {
        // console.log('filesList 1', filesList);
        // console.log('index', index);
        
        filesList[index].files.push(files[i]);
        const fileURL = URL.createObjectURL(files[i]);
        const extension = fileURL.split('.').pop().split(/[\?#]/)[0]; // получаем часть после последней точки.   

        console.log('File extension:', extension);
        // $(`#${field.ulId}`).append(`<li>${files[i].name}</li>`);  // Отображаем имена файлов
        if (extension == 'pdf') {
            $(`#files-list-block-${index+1}`).append(`
                <img id="files-list-image-${index+1}-${i+1}" 
                class="files-list-image" src="${pdfFile}" 
                alt="${files[i].name}" 
                onclick="selectFile(${index}, ${filesList[index].files.length - 1}, '${fileURL}')">
                `)

        } else if (extension == 'mp4' || extension == 'webm') {
            $(`#files-list-block-${index+1}`).append(`
                <img id="files-list-image-${index+1}-${i+1}" 
                class="files-list-image" src="${videoFile}" 
                alt="${files[i].name}" 
                onclick="selectFile(${index}, ${filesList[index].files.length - 1}, '${fileURL}')">
                `)

        } else {
            $(`#files-list-block-${index+1}`).append(`
                <img id="files-list-image-${index+1}-${i+1}" 
                class="files-list-image" src="${fileURL}" 
                alt="${files[i].name}" 
                onclick="selectFile(${index}, ${filesList[index].files.length - 1}, '${fileURL}')">
                `)
        }
        
    }
}


