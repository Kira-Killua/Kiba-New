# 欢迎使用KibaBot New(Kiba V4)!

<img src="https://img.shields.io/github/license/Kira-Killua/Kiba-New" alt="license">

本项目基于 Yuri-YuzuChaN 的 maimaiDX 项目。特此表示感谢。

maimaiDX 项目移植自 xybot 及 [mai-bot](https://github.com/Diving-Fish/mai-bot) 开源项目。

KibaBot New 是基于 [HoshinoBotV2](https://github.com/Ice-Cirno/HoshinoBot) 的街机音游 **舞萌DX** 的查询插件，
当前正在运营的 KibaBot 使用了特殊精简的 HoshinoBotV2 框架。但此项目可以正常在标准的 HoshinoBotV2 框架上运行。

maimaiDX 项目地址：https://github.com/Yuri-YuzuChaN/maimaiDX

Kiba 旧框架项目：https://github.com/Kira-Killua/Kiba-Old-

Kiba 新框架：https://github.com/Kira-Killua/Kiba-New


## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目
   
    ``` git
    git clone https://github.com/Kira-Killua/Kiba-New
    ```
    
2. 下载静态资源文件，将该压缩文件解压后，将 `static` 文件夹复制到插件根目录并覆盖，即 `maimaiDX/static` 并覆盖，[下载链接](https://share.yuzuchan.moe/d/aria/Resource.zip?sign=LOqwqDVm95dYnkEDYKX2E-VGj0xc_JxrsFnuR1BcvtI=:0)
3. 如果您拥有查分器的开发者 `token`，可修改 `maimaiDX/static/config.json` 文件，将 `token` 填入文件
4. 安装插件所需模块：`pip install -r requirements.txt`
5. 在 https://phantomjs.org/download.html 下载对应操作平台PhantomJS支持，`windows` 平台需要添加环境目录
6. 在 `config/__bot__.py` 模块列表中添加 `KibaBot-New`（存档的文件夹名字）
7. 重启HoshinoBot

## 指令

| 命令                                             | 功能                            |
|------------------------------------------------|-------------------------------|
| 帮助maimaiDX                                     | 查看指令帮助                        |
| 今日舞萌                                           | 查看今天的舞萌运势                     |
| XXXmaimaiXXX什么                                 | 随机一首歌                         |
| 随个[dx/标准][绿黄红紫白]<难度>                           | 随机一首指定条件的乐曲                   |
| 查歌<乐曲标题的一部分>                                   | 查询符合条件的乐曲                     |
| id<歌曲编号>                                | 查询乐曲信息或谱面信息                   |
| <歌曲别名>是什么歌                                     | 查询乐曲别名对应的乐曲                   |
| <id/歌曲别称>有什么别称                                 | 查询歌曲别名                        |
| 添加本地别名 <歌曲ID> <歌曲别名>                         | 添加本地别名，不上传别名服务器         |
| 添加别称 <歌曲ID> <歌曲别名>                             | 申请添加歌曲别名                      |
| 当前别名投票 <页数>                                        | 查看正在进行的投票                     |
| 同意别名 <标签>                                      | 同意其中一个标签的别名申请，可通过指令 当前别名投票 查看 |
| 开启/关闭别名推送                                      | 开启或关闭新别名投票的推送                 |
| 定数查歌 <定数> 定数查歌 <定数下限> <定数上限>                   | 查询定数对应的乐曲                     |
| 分数线 <难度+歌曲id> <分数线>                            | 展示歌曲的分数线                      |
| 开启/关闭mai猜歌                                     | 开关猜歌功能                        |
| 重置猜歌                                            | 停止当前进行的猜歌                  |
| 猜歌                                             | 顾名思义，识别id，歌名和别称               |
| 猜曲绘                                            | 猜曲绘                                |
| minfo<@> <id/别称/曲名>                            | 查询单曲成绩                        |
| ginfo[绿黄红紫白] <id/别称/曲名>                        | 查询乐曲游玩总览，不加难度默认为紫谱         |
| b50 <游戏名>                                      | 查询b50                         |
| 我要在<难度>上<分数>分 <游戏名>                            | 查看推荐的上分乐曲                     |
| 我要(在<难度>)上<分数>分 <名字>                           | 查看推荐的上分乐曲                     |
| <牌子名称>进度 <名字>                                  | 查看牌子完成进度                      |
| <等级><评价>进度 <名字>                                | 查看等级评价完成进度                    |
| <等级> 分数列表 <名字>                                 | 查看等级评价列表                      |
| 查看排名,查看排行 <页数>/<名字>                            | 查看水鱼网站的用户ra排行                 |
| 添加机厅 <店名> <位置> <机台数量>                     | 添加机厅信息                        |
| 删除机厅 <店名>                                      | 删除机厅信息                        |
| 修改机厅 <店名> 数量 <数量>                           | 修改机厅信息                        |
| 订阅机厅 <店名>                                      | 订阅机厅，简化后续指令                   |
| 查看订阅                                           | 查看群组订阅机厅的信息                   |
| 取消订阅,取消订阅机厅                                    | 取消群组机厅订阅                      |
| 添加机厅别名 <店名> <别名>                                | 添加机厅别名                      |
| 查找机厅,查询机厅,机厅查找,机厅查询 <关键词>                      | 查询对应机厅信息                      |
| <店名/别名>人数设置,设定,增加,加,+,减少,减,-<人数>                  | 操作排卡人数                        |
| <店名/别名>有多少人,有几人,有几卡,几人,几卡                         | 查看排卡人数                        |
| 全局[关闭/开启]别名推送                               | Bot管理员私聊指令，开关所有群的别名推送   |
| 更新别名库                                            | Bot管理员私聊指令，手动更新别名库   |
| 更新maimai数据                                            | Bot管理员私聊指令，手动更新已存所有数据  |

## 更新说明

**KibaBot New 4.1 (Kiba 4.1)**

1.修复 Bug

2.更细致的 Best 50 页面

3.更细致的歌曲详情页


**KibaBot New (Kiba 4.0)**
1. 框架更换至HoshinoBot。
2. 同步 maimaiDX 项目更新至 2024-06-07。
3. 重新匹配的美术资源、新的歌曲详情页。
4. 修复歌曲详细页素材错位问题。
5. KibaNew框架 Best50 排版更新。



## 鸣谢

感谢 [Yuri-YuzuChaN](https://github.com/Yuri-YuzuChaN/) 提供的源码支持

感谢 [zhanbao2000](https://github.com/zhanbao2000) 提供的 `nonebot2` 分支

感谢 [CrazyKid](https://github.com/CrazyKidCN) 提供的源码支持

感谢 [Diving-Fish](https://github.com/Diving-Fish) 提供的源码支持

感谢 [BlueDeer233](https://github.com/BlueDeer233) 提供猜歌功能的源码支持

## License

MIT

您可以自由使用本项目的代码用于商业或非商业的用途，但必须附带 MIT 授权协议。
