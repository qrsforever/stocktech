---

title: 数据分析笔记

date: 2019-05-17 20:37:01
tags: [notebook]
categories: [stocktech]

---

## Jupyter

### Install

    sudo pip3 install -U jedi
    sudo pip3 install -U jupyter pyside2 pyqt5
    sudo pip3 install -U jupyter_contrib_nbextensions jupyter_nbextensions_configurator
    sudo pip3 install -U jupyterthemes
    sudo jupyter contrib nbextension install
    sudo jupyter nbextensions_configurator enable


### vim support

    mkdir -p $(jupyter --data-dir)/nbextensions
    cd $(jupyter --data-dir)/nbextensions
    git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding
    chmod -R go-w vim_binding
    jupyter nbextension enable vim_binding/vim_binding


### use in vim

配置请参考我的[vim配置][1]

### use in console

    jupyter notebook --notebook-dir=. --port=9182 --browser='opera %s'


## Other


[1]: https://github.com/qrsforever/vim/blob/master/bundle/.configs/jupyter-vim_conf.vim

