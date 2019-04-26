---

title: 爬取股票信息

date: 2019-04-11 15:03:18
tags: [crawl]
categories: [stock]

---

# 准备

1. `sudo pip3 install -U fake-useragent`
2. `sudo pip3 install -U scrapy-splash`
3. `sudo docker run -p 8050:8050 scrapinghub/splash --max-timeout`

# 创建工程

```
scrapy startproject crawlstocks .
--logfile=xxx/crawl.log
--loglevel=DEBUG
--pidfile=xxx/crawl.pid
```


# 创建网虫

- `scrapy genspider [--template=crawl] xxx hq.gucheng.com`

# 执行

`scrapy list`

```
2019-04-26 17:08:10 [stdout] INFO eastmoney.cwzb
2019-04-26 17:08:10 [stdout] INFO eastmoney.url
2019-04-26 17:08:10 [stdout] INFO gucheng.blockcode
2019-04-26 17:08:10 [stdout] INFO gucheng.financialinfo
2019-04-26 17:08:10 [stdout] INFO gucheng.stockcode
2019-04-26 17:08:10 [stdout] INFO netease163.chddata
```

- 下载所有的股票码, 供下面的几个模块使用: `scrapy crawl gucheng.stockcode`

- 下载股城网个股财务信息: `scrapy crawl gucheng.financialinfo`

- 从东方财富网下载个股的URLS: `scrapy crawl eastmoney.url`

- 下载财务数据: `scrapy crawl eastmoney.cwzb -a filename=xxx/xxx/stock_urls.txt`

   **依赖scrapy-splash,实现异步转同步**

[获取settings方式](https://blog.csdn.net/weixin_40841752/article/details/82900326)

# 网虫

## GuchengStockList

从股城网爬取当日所有股票码和股票名字, 分别存到文件`stock_codes.txt`和mongo数据库
`stock.codes`中.

## QuotesMoney163

从网易财经行情中心爬取个股的历史数据, 具体日期范围由`settings.py`设置,数据存到mongo数
据库`stock.chddata`中.


# 数据网站

## 股城网(hq.gucheng.com)

## 东方财富网(quote.eastmoney.com)

2019.04之后`https://quote.eastmoney.com/stocklist.html`已经不能方便获取所有股票信息了,
可以结合股城网一起爬取数据.

(封号严重)

1. 股城网爬取所有股票的代码, 保存到文件中
2. 东方财富网根据具体的股票代码获取更多的信息, 把1中的文件通过-a NAME=VALUE传给spider

# Shell调试Selector

```html <section class="stockTable"> <h3>上海深圳股票代码一览表</h3> <a
href="https://hq.gucheng.com/SZ000001/">平安银行(000001)</a> <a
href="https://hq.gucheng.com/SZ000002/">万 科A(000002)</a> <a
href="https://hq.gucheng.com/SZ000004/">国农科技(000004)</a> <a
href="https://hq.gucheng.com/SZ000005/">世纪星源(000005)</a> </section> ```

``` # scrapy shell In[1]: fetch('https://hq.gucheng.com/gpdmylb.html') In[2]:
response.xpath('//section[has-class("stockTable")]/a/text()').get() ```

# 参考

1. [爬虫入门](https://www.cnblogs.com/derek1184405959/p/8451798.html)
2. [Scrapy文档](https://doc.scrapy.org/en/latest/intro/overview.html)
3. [Selector](https://docs.scrapy.org/en/latest/topics/selectors.html)
4. [随机代理](https://www.cnblogs.com/trunkslisa/p/9841658.html)

# 问题

## 动态页面

[how to scrape the dynamic website using scrapy][1]
[Scraping dynamic content using python-Scrapy][2]
[Splash][3]
[Scrapy+Splash实例][4]

[1]: https://medium.com/@vigneshgig/how-to-scrape-the-dynamic-website-using-sitemap-731f5e4651a9
[2]: https://stackoverflow.com/questions/30345623/scraping-dynamic-content-using-python-scrapy
[3]: https://splash.readthedocs.io/en/stable
[4]: https://github.com/scrapy-plugins/scrapy-splash
