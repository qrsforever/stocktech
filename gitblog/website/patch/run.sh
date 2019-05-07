#!/bin/bash

# npm install hexo-renderer-mathjax
# npm install hexo-renderer-kramed
# npm install kramed

# cp ./hexo-renderer-kramed/renderer.js ../node_modules/hexo-renderer-kramed/lib/
# cp ./kramed/inline.js ../node_modules/kramed/lib/rules/
cp ./hexo-renderer-mathjax/mathjax.html ../node_modules/hexo-renderer-mathjax/
cp ./hexo-jupyter-notebook/main.py ../node_modules/hexo-jupyter-notebook/
cp ./hexo-jupyter-notebook/index.js ../node_modules/hexo-jupyter-notebook/
# cp ./gitment/gitment.js ../node_modules/gitment/dist/
# 或者修改：themes/hexo-theme-indigo/layout/_partial/plugins/gitment.ejs
