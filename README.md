# 介绍
苍龙三国志服务器发布工具是一款带有图形界面的工具软件，旨在提高服务器程序的工作效率，让策划能够很方便地自行更新各版本服务器配置表，后续还会添加服务器代码一键发布等功能。


# 代码结构

+ design
 - publish_tool.fbp 使用wxFormBuilder制作的界面布局
+ env.py 环境参数
+ publish.py 发布操作
+ sftp.py 上传下载及执行sh命令组件
+ tool_start.py 工具启动文件
+ ui.py 通过wxFormBuilder生成的wxPython界面，请勿直接修改

# 详细说明
见苍龙智库文章[苍龙服务器发布工具gui版出炉啦](http://192.168.2.118/wordpress/2017/11/15/苍龙服务器发布工具gui版出炉啦/)