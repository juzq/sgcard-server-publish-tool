#!/bin/bash
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/06
# Description: 在screen中开启服务器
# ------------------------------------------------------------------------------

server_id=$1

expect -c "
set timeout 60
spawn screen -r -d ${server_id}
expect {
	# 没有screen
	\"no screen\" {
		exit
    }
    # 有screen
    "\*]$" {
    	send \"stop\r\"
		expect {
			# 上次启动出现异常
			\"Exception\" {
				send  \"\003\"
				sleep 30
				send \"exit\r\"
			}
			# 等待关服成功
			\"application will exit\" {
				sleep 3
				send \"exit\r\"
			}
			# 已经关闭
			\"missing job name\" {
				sleep 1
				send \"exit\r\"
			}
			# 已经关闭
			\"command not found\" {
				sleep 1
				send \"exit\r\"
			}
		}
    }
}

expect eof"

