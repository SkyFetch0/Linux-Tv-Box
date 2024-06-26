const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'script.js'), 
      nodeIntegration: true,
      contextIsolation: false
    },
    fullscreen: true, 
    autoHideMenuBar: true 
  });

  mainWindow.loadFile('index.html');
}

function createYoutube() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            webviewTag: true
            
        },
        fullscreen: true, 
        autoHideMenuBar: true 
    });
    
      mainWindow.loadFile('youtube.html');
}

function createGoogle() {
const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
        webviewTag: true,
        preload: path.join(__dirname, 'google.js'), 
        nodeIntegration: false, 
        contextIsolation: true, 
        enableRemoteModule: false 
    },
    fullscreen:true ,
    autoHideMenuBar: true 
});
mainWindow.loadFile('google.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('selected-item', (event, data) => {
  console.log('Selected item data-href:', data);

  if (data === 'open_youtube') {
    createYoutube();
  } else if(data === 'open_google') {
    createGoogle();
  }
 
});
