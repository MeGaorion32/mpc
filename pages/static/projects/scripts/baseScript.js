const toggleDropdown = document.getElementById('toggle-dropdown');        
const logoutBlock = document.getElementById('logout-button-block');        

toggleDropdown.addEventListener('click', function() {        
    // Переключаем видимость кнопки выхода        
    if (logoutBlock.style.display === 'none' || logoutBlock.style.display === '') {        
        logoutBlock.style.display = 'flex';        
    } else {        
        logoutBlock.style.display = 'none';        
    }        
});   

 // Скрыть прелодер после полной загрузки страницы
 window.addEventListener('load', function() {
    document.getElementById('preloader').style.display = 'none';
});
       