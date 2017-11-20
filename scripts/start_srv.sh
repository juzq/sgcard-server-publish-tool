#!/bin/bash
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/06
# Description: 在screen中开启服务器
# ------------------------------------------------------------------------------

server_type=$1
server_id=$2

# 进入目录
cd /home/honor/online/${server_type}Srv/${server_id}

sh_name=
expect_str=
if [[ ${server_type} == "game" ]]; then
	sh_name="GameServer.sh"
	expect_str="GameServer Started"
elif [[ ${server_type} == "fight" ]]; then
	sh_name="FightServer.sh"
	expect_str="fightServer startup"
elif [[ ${server_type} == "list" ]]; then
	sh_name="ListServer.sh"
	expect_str="启动完毕"
fi

# 在screen里启动
expect -c "
set timeout 60
spawn screen -R ${server_id}
sleep 1
send \"sh ${sh_name}\r\"
expect {
	\"${expect_str}\" {
		send \"gm 1\r\"
	}
	\"Exception\" {
	}
}
sleep 1
send  \"\001\"
send \"d\"
expect eof"

