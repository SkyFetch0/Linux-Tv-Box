const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('apps').classList.add('selected');

    let menuMode = true; 
    function playSelectSound() {
        const selectSound = new Audio('./assets/mp3/menu1.mp3');
        selectSound.play();
    }

    document.addEventListener('keydown', function(event) {
        const current = document.querySelector('.selected');
        let next;

        if (menuMode) {
           
            const menuItems = document.querySelectorAll('.side-menu .nav-link');
            const currentMenuIndex = Array.from(menuItems).findIndex(item => item === document.querySelector('.side-menu .selected'));

            if (event.key === 'w' || event.key === 'ArrowUp' || event.key === "ArrowLeft") {
                next = currentMenuIndex > 0 ? menuItems[currentMenuIndex - 1] : null;
            } else if (event.key === 's' || event.key === 'ArrowDown' || event.key === "ArrowRight") {
                next = currentMenuIndex < menuItems.length - 1 ? menuItems[currentMenuIndex + 1] : null;
            }

            if (event.key === 'e') {
                menuMode = false; 
            }
        } else {
            const cards = document.querySelectorAll('.col-sm-6 .card');
            const currentIndex = Array.from(cards).findIndex(card => card.classList.contains('selected'));

            if (event.key === 'w' || event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
                next = currentIndex > 0 ? cards[currentIndex - 1] : null;
            } else if (event.key === 's' || event.key === 'ArrowDown' || event.key === 'ArrowRight') {
                next = currentIndex < cards.length - 1 ? cards[currentIndex + 1] : null;
            }

            if (event.key === 'e') {
                menuMode = true; 
            }
        }

        if (next) {
            current.classList.remove('selected');
            next.classList.add('selected');
            playSelectSound(); 
        }

        if(event.key === "Enter") {
            ipcRenderer.send('selected-item', current.dataset.href);
        }
    });
});
