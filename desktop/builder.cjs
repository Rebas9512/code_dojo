const path = require('node:path')
const shared = path.resolve(__dirname, '../scripts/desktop')

module.exports = {
  appId: 'local.code-dojo.desktop',
  productName: 'code-dojo',
  files: ['main.cjs', 'preload.cjs', 'startup.*', 'fonts/**'],
  extraResources: [
    { from: process.env.CODE_DOJO_RESOURCES, to: 'runtime' },
    { from: path.join(shared, 'code-dojo.png'), to: 'code-dojo.png' },
  ],
  npmRebuild: false,
  publish: null,
  linux: { target: ['tar.gz'], category: 'Education', icon: path.join(shared, 'code-dojo.png'),
    artifactName: 'code-dojo-${version}-x86_64-linux.tar.gz' },
  mac: { target: ['zip'], identity: null, icon: 'icon.png', artifactName: 'code-dojo-${version}-arm64-mac.zip' },
  win: { target: ['zip'], icon: path.join(shared, 'code-dojo.png'), artifactName: 'code-dojo-${version}-x64-windows.zip' },
}
