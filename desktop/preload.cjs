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
      close: () => ipcRenderer.invoke('startup:close'),
      browseAgent: () => ipcRenderer.invoke('startup:browse-agent'),
      setAgentPath: (agent, path) => ipcRenderer.invoke('startup:agent-path', agent, path),
      subscribe: callback => { ipcRenderer.on('startup:state', (_event, state) => callback(state)) },
      connectSync: code => ipcRenderer.invoke('startup:connect', code),
      disconnectSync: () => ipcRenderer.invoke('startup:disconnect'),
      retry: () => ipcRenderer.invoke('startup:retry'),
    })
  }
}
