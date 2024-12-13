let fieldsList = [
    { buttonId: 'photo-upload-button', inputId: 'photo-file-input', ulId: 'photo-file-list', label: 'Добавить фото'},
    { buttonId: 'video-upload-button', inputId: 'video-file-input', ulId: 'video-file-list', label: 'Добавить видео'},
    { buttonId: 'graphic-upload-button', inputId: 'graphic-file-input', ulId: 'graphic-file-list', label: 'Добавить графики'},
    { buttonId: 'summary-upload-button', inputId: 'summary-file-input', ulId: 'summary-file-list', label: 'Добавить сводки'},
    { buttonId: 'techpark-upload-button', inputId: 'techpark-file-input', ulId: 'techpark-file-list', label: 'Добавить парк техники'},
    { buttonId: 'personal-upload-button', inputId: 'personal-file-input', ulId: 'personal-file-list', label: 'Добавить персонал ВЗис'},
    { buttonId: 'equipment-upload-button', inputId: 'equipment-file-input', ulId: 'equipment-file-list', label: 'Добавить оснащение'},
    { buttonId: 'laboratory-upload-button', inputId: 'laboratory-file-input', ulId: 'laboratory-file-list', label: 'Добавить лаборатория'},
    { buttonId: 'ot_pb_oos-upload-button', inputId: 'ot_pb_oos-file-input', ulId: 'ot_pb_oos-file-list', label: 'Добавить ОТ ПБ ООС'},
    { buttonId: 'regulation-upload-button', inputId: 'regulation-file-input', ulId: 'regulation-file-list', label: 'Добавить предписания'},
    { buttonId: 'reserv-upload-button', inputId: 'reserv-file-input', ulId: 'reserv-file-list', label: 'Добавить резервная позиция'},
]; 
let filesList = [
    { name: 'photo', files: [] },
    { name: 'video', files: [] },
    { name: 'graphics', files: [] },
    { name: 'summaries', files: [] },
    { name: 'techpark', files: [] },
    { name: 'personal', files: [] },
    { name: 'equipment', files: [] },
    { name: 'laboratories', files: [] },
    { name: 'ot_pb_oos', files: [] },
    { name: 'regulations', files: [] },
    { name: 'reserv', files: [] },
]; 

let filesBlock = $('#files-block');

console.log('projectFiles', projectFiles);



function getFilesBlock() {
    let fileBlockItem = ``
    fieldsList.forEach((field, index) => {
        if (field.inputId == 'photo-file-input') {
            fileBlockItem = `
            <button id="${field.buttonId}" class="file-input-button btn btn-primary">${field.label}</button>
            <input type="file" id="${field.inputId}" multiple style="display: none;" accept="image/png, image/jpeg, image/jpg"/>
            <ul id="${field.ulId}"></ul>   
            <div id="files-list-block-${index+1}" class="files-list-block"></div>         
        `
        } else if (field.inputId == 'video-file-input') {
            fileBlockItem = `
            <button id="${field.buttonId}" class="file-input-button btn btn-primary">${field.label}</button>
            <input type="file" id="${field.inputId}" multiple style="display: none;" accept="video/mp4, video/webm"/>
            <ul id="${field.ulId}"></ul>   
            <div id="files-list-block-${index+1}" class="files-list-block"></div>`
        } else {
            fileBlockItem = `
            <button id="${field.buttonId}" class="file-input-button btn btn-primary">${field.label}</button>
            <input type="file" id="${field.inputId}" multiple style="display: none;" accept="application/pdf, text/plain"/>
            <ul id="${field.ulId}"></ul>   
            <div id="files-list-block-${index+1}" class="files-list-block"></div>`
        }
        
        filesBlock.append(fileBlockItem)
    })
}

getFilesBlock();

// Функция для отображения существующих файлов
function displayExistingFiles() {
    projectFiles.forEach(file => {       

        filesList.forEach((listFile, index) => {
            // console.log('listFile.name', listFile.name);
            // console.log('file.type.toLowerCase()', file.type.toLowerCase());
            
            if (listFile.name === file.type.toLowerCase()) {
                // listFile.files.push(file);
                const fileURL = file.full_file_path;
                $(`#files-list-block-${index + 1}`).append(`
                    <img class="files-list-image" 
                    id="files-list-image-${file.id}"
                    src="${fileURL}" 
                    alt="${file.path}" 
                    onclick="selectFile(${index}, ${listFile.files.length}, '${fileURL}', '${file.id}')">
                `);
                // listFile.files.push(file.full_file_path);
            }
           
        })


    });
}

// Вызов функции для отображения существующих файлов
displayExistingFiles();
