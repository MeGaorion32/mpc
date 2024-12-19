// Получаем элементы
var modal = document.getElementById("menu-modal");
var hamburger = document.getElementById("hamburger");
var closeBtn = document.getElementById("menu-modal-close");

// Открыть модальное окно при нажатии на гамбургер
hamburger.onclick = function() {
    modal.style.display = "block";
}

// Закрыть модальное окно при нажатии на "x"
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// Закрыть модальное окно при клике вне его
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
