可以自动运行，支持连续做题的平安京学历测试题库爬虫

需要的环境和工具：

```shell
Python 3.5+
selenium
pyquery
chromedriver
```

安装教程见：<https://www.cnblogs.com/eternal1025/p/8880245.html>

运行：

```shell
python app.py 
```

进入题目，开始答题状态后台挂机即可（在首页初次加载完后台挂机会出错）

答案会在answer.txt里，格式：问题 |选项 # 答案

更新：
增加可以直接通过adb操作设备爬取大神题目的脚本（未登录和已登陆题库不同），需要用到poco
安装：
```shell
pip3 install pocoui
```

进入答题准备界面，启动即可：

```shell
python appWithPocoui.py
```

（理论上可以做到自动答题）