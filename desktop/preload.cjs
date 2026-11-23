const { contextBridge, ipcRenderer } = require('electron')

if (process.isMainFrame) {
  contextBridge.exposeInMainWorld('dojoDesktop', {
    sync: () => ipcRenderer.invoke('dojo:sync'),
    settings: () => ipcRenderer.invoke('dojo:settings'),
    about: () => ipcRenderer.invoke('dojo:about'),
    quit: () => ipcRenderer.invoke('dojo:quit'),
    version: () => ipcRenderer.invoke('dojo:version'),
  })
  if (location.protocol === 'file:') {
    contextBridge.exposeInMainWorld('dojoStartup', {
      read: () => ipcRenderer.invoke('startup:read'),
      subscribe: callback => { ipcRenderer.on('startup:state', (_event, state) => callback(state)) },
      unlock: password => ipcRenderer.invoke('startup:unlock', password),
      tokens: (code, sync) => ipcRenderer.invoke('startup:tokens', code, sync),
      retry: () => ipcRenderer.invoke('startup:retry'),
    })
  }
}
