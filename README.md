---

title: 股科系统

date: 2019-04-25 21:32:12

tags: [stock]
categories: [stocktech]

---


# setup

```sh
export STOCKTECH_DIR=`pwd`
```

# 准备

参考各子目录


# 顶级目录

- `scrapy`

爬虫, 数据存储

- `selenium`

web自动化操作, 登录页面/解析/存储, 解决scrapy对cookie登录无效的取代方案

- `reminder`

股票信息提醒,包括习大大最新新闻提醒, mosquito(MQTT服务代理), eye3(安卓app, 提示震动)

- `notebook`

对股票数据库的数据做简单分析, 为调试方便可以采用jupyter-vim或者jupyter, 大大方便coding

- `core`

核心算法


- `gitblog`

Github博客, 用来展示数据分析的结果

- `tushare`

一个社区, 封装很多股市数据的api, 通过积分验证权限

- `output`

null

