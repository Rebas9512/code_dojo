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
  mac: {
    target: ['zip'], identity: '-', notarize: false, icon: 'icon.png', artifactName: 'code-dojo-${version}-arm64-mac.zip',
    // hardened runtime 只在公证时需要；关掉后随包 Python 加载判题环境里未签名的扩展库，行为和 1.3.0 一样。
    hardenedRuntime: false,
    // osx-sign 也把字节码等数据识别成二进制。它们由整包签名封存，只有原生代码需要单独签。
    signIgnore: ['/Contents/Resources/runtime/.*\\.(pyc|py|a|o|exe|whl|gif|png|ico|gz)$'],
  },
  win: { target: ['zip'], icon: path.join(shared, 'code-dojo.png'), artifactName: 'code-dojo-${version}-x64-windows.zip' },
}
