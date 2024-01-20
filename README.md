<div align="center">

![botpy](https://socialify.git.ci/tencent-connect/botpy/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&language=1&logo=https%3A%2F%2Fgithub.com%2Ftencent-connect%2Fbot-docs%2Fblob%2Fmain%2Fdocs%2F.vuepress%2Fpublic%2Ffavicon-64px.png%3Fraw%3Dtrue&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light)

![Python](https://img.shields.io/badge/python-3.8+-blue)

_✨ 基于 [机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的机器人框架 ✨_

_✨ 为开发者提供一个易使用、开发效率高的开发框架 ✨_

[官方文档](https://bot.q.qq.com/wiki/develop/pythonsdk/)
·
[阿斯巴迪机器人频道](https://pd.qq.com/s/hgrekb2ag)
·
[机器人后台](https://q.qq.com)

</div>

# 阿斯巴迪机器人

 使用前先参考官方python sdk即botpy

### QQ机器人botpy，阿斯巴迪机器人，基于官方python sdk开发的公域机器人

# 阿斯巴迪机器人文件介绍（⑩山代码）

>azhu.py 主要代码运行程序

>bltxt.py 这个是主要的聊天系统

>cqsp.py 群端机器人发送视频示例

>dxt.py 这个是群聊和频道端系统状况代码（根据具体情况选择性抛弃）

>config.yaml 鉴权登录需要

# 注意
>### azhu.py里面包含了群事件监听，包含了一堆依赖，需要自主安装

>### 如没有群事件监听权限，记得修改代码

>需要修改删除群监听部分代码，以及代码最后的监听通道

