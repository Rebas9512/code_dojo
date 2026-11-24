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
      connectSync: code => ipcRenderer.invoke('startup:connect', code),
      disconnectSync: () => ipcRenderer.invoke('startup:disconnect'),
      retry: () => ipcRenderer.invoke('startup:retry'),
    })
  }
}
