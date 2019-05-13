---

title: 浏览器自动化

date: 2019-04-30 11:19:02
tags: [selenium]
categories: [stock]

---

# Install

- [`sudo pip3 install -U selenium`](https://seleniumhq.github.io/selenium/docs/api/py/)

- `sudo pip3 install -U beautifulsoup4`

- [`wget geckodriver`](https://github.com/mozilla/geckodriver/releases)

    ```shell

    bin
    ├── geckodriver_linux32_v0.24.0
    ├── geckodriver_linux64_v0.24.0
    ├── geckodriver_win32_v0.24.0
    └── geckodriver_win64_v0.24.0

    ```

- [`sudo apt-get install xvfb`](https://www.cnblogs.com/happyday56/p/9006629.html)

    无界面自动化

- [`sudo pip3 install xvfbwrapper`](https://cloud.tencent.com/developer/ask/107705)

    无界面自动化(推荐)

# Usage

- `./main.py list`

- `./main.py crawl task` or `./main.py 1`

# Crawl

## `crawl_tencent_optional` in `tencent_optional.py`

自动登录hu.qq.com将自选股票代码下载到`settings.OPTIONAL_CODES_FILE`

