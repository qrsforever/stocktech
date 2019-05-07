## installer

- `sudo apt-get install pandoc texlive`
- `sudo pip3 install -U nbconvert`
- `sudo apt-get install nodejs npm`
- `sudo npm install hexo-cli -g`

## 设置

- `npm install`
- `cd patch; ./run`
- `hexo clean`: 清理
- `hexo g`: 生成
- `hexo s`: 本地服务,预览
- `hexo d`: 发布到github

## 文档目录

`source/_posts`

## 多个github账号keys的管理

1. 创建RSA

- `ssh-keygen -t rsa -b 4096 -C "985612771@qq.com"`
- `ssh-add -D` 删除
- `ssh-add ~/.ssh/id_rsa_zytblog`
- `ssh-add -l` 列出


2. 编辑`cat ~/.ssh/config`

```
Host zytforever.github.com
    HostName         github.com
    PreferredAuthentications   publickey        
    User             git
    IdentityFile     /home/lidong/.ssh/id_rsa_zytblog
```

3. 编辑`cat website/_config.yml`

```
deploy:
    type: git
    repo: git@zytforever.github.com:zytforever/zytforever.github.io.git
    branch: master
```
