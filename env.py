# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 环境设置
# ------------------------------------------------------------------------------

import subprocess
import os

server_info = {
    '测试': {
        'release_en': 'test',
        'ip': '192.168.60.169',
        'port': 22,
        'fight_ip': '192.168.60.169',
        'username': 'honor',
        'password': 'xx'
    },
    '日文': {
        'release_en': 'jp',
        'ip': '210.73.210.83',
        'port': 4399,
        'fight_ip': '210.73.210.83',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '韩文': {
        'release_en': 'kr',
        'ip': '210.73.210.93',
        'port': 4399,
        'fight_ip': '210.73.210.94',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '台湾': {
        'release_en': 'hk',
        'ip': '210.73.210.93',
        'port': 4399,
        'fight_ip': '210.73.210.94',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '东南亚': {
        'release_en': 'sea',
        'ip': '210.73.210.93',
        'port': 4399,
        'fight_ip': '210.73.210.94',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '内网': {
        'release_en': 'inner',
        'ip': '192.168.2.118',
        'port': 22,
        'fight_ip': '192.168.2.118',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    }
}


remote_root_path = '/home/honor/online/'
tool_path = '\\tool_build'
build_path = tool_path + '\\build'
source_path = '\\src'
config_path = '\\config'
source_list_file = 'sources.list'
copy_source_path = '\\com\\xd100\\lzll\\db\\sqlmap'
package_path = tool_path + '\\bin.zip'
work_path = os.path.expanduser('~') + '\\CL_Srv_Pub_Tool'
work_config_path = work_path + '\\config'
work_history_path = work_path + '\\history'
work_config_release = 'release'
work_config_srv_type = 'srv_type'
work_config_dir_path = 'dir_path'
work_config_jdk_path = 'jdk_path'
work_config_upload_csv = 'upload_csv'


# 检查jdk路径
def check_java(jdk_path):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if jdk_path is None:
        cmd = 'java -version'
    else:
        cmd = '"' + jdk_path + '\\bin\\java" -version'
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=si)
    line = str(p.stdout.readline())
    if 'version' in line:
        return line.replace('b\'java version ', '').replace('\\r\\n\'', '')
    else:
        return None
