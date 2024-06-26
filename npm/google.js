const { contextBridge, ipcRenderer } = require('electron');

var webview = document.getElementById('googleWebview');
webview.addEventListener('dom-ready', function () {
    function injectCSS(cssFilePath) {
        fetch(cssFilePath)
            .then(response => response.text())
            .then(cssContent => {
                const styleElement = document.createElement('style');
                styleElement.textContent = cssContent;
                webview.shadowRoot.appendChild(styleElement); 
            })
            .catch(error => {
                console.error('CSS dosyası yüklenirken bir hata oluştu:', error);
            });
    }

    injectCSS('google.css');
});


contextBridge.exposeInMainWorld('electron', {
// Hello World :d
});