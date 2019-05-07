
const path = require('path')
const exec = require('co-exec')
const co = require('co')
const fs = require('co-fs')
const PY_SCRIPT = path.join(__dirname, 'main.py')

hexo.extend.tag.register('asset_jupyter', function (args) {
  const post = this
//   console.log(args)


  return co(function *() {
    const PYTHON_ENV = args[0]
    // const jupyterFile = path.join(post.asset_dir, args[1])
    // console.log(jupyterFile)
    // lidong mod.
    // let html = yield exec(`${PYTHON_ENV} ${PY_SCRIPT} ${jupyterFile}`, {
    let html = yield exec(`${PYTHON_ENV} ${PY_SCRIPT} ${post.asset_dir} ${args[1]}`, {
      maxBuffer: 50 * 1024 * 1024,
      env: {
        PYTHONIOENCODING: 'utf8'
      }
    })

    // console.log(html.length)
    return html
  })

}, {
  async: true,
  ends: false
})
