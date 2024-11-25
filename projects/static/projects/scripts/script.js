console.log('Test');

// Обработчик клика для открытия изображения в модальном окне

function openFile(type, file_path) {
    const modal = document.getElementById('fileModal');
    const modalImg = document.getElementById('modalImage');
    const modalPdf = document.getElementById('modalPdf');
    modal.style.display = "block";
    if (type == 'img') {
        modalImg.style.display = "block";
        modalPdf.style.display = "none"; // скрываем PDF
        modalImg.src = file_path;
    } else if (type == 'pdf') {
        // modalPdf.src = "{% static 'projects/ViewerJS/index.html' %}#{{ project.full_file_path }}";
        modalPdf.style.display = "block"; // показываем PDF
        modalImg.style.display = "none"; // скрываем изображение
        modalPdf.src = file_path;
    }

}

// document.querySelector('#projectImage').addEventListener('click', function() );


// document.querySelector('#projectImage').addEventListener('click', function() {
//     const modal = document.getElementById('fileModal');
//     const modalImg = document.getElementById('modalImage');
//     modal.style.display = "block";
//     modalImg.src = "{{ project.full_file_path }}";
// });

  // Обработчик клика для открытия PDF в модальном окне
//   document.querySelector('#projectPdf').addEventListener('click', function() {
//     const modal = document.getElementById('fileModal');
//     const modalPdf = document.getElementById('modalPdf');
//     modal.style.display = "block";
//     modalPdf.src = "{% static 'projects/ViewerJS/index.html' %}#{{ project.full_file_path }}";
// });

 // Закрытие модального окна
 document.getElementById('closeFileModal').onclick = function() {
    console.log('close');        
    // document.getElementById('fileModal').style.display = "none";
    const modal = document.getElementById('fileModal');
    modal.style.display = "none";
    const modalImg = document.getElementById('modalImage');
    const modalPdf = document.getElementById('modalPdf');    

    // Очистка содержимого модала
    modalImg.src = "";
    modalPdf.src = "";
    modalImg.style.display = "none";
    modalPdf.style.display = "none";
}


// Перетаскивание модального окна
dragElement(document.getElementById("fileModal"));

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

