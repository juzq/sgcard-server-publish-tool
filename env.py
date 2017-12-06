# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 环境设置
# ------------------------------------------------------------------------------

import subprocess

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
source_list_file = 'sources.list'
copy_source_path = '\\com\\xd100\\lzll\\db\\sqlmap'
package_path = tool_path + '\\bin.zip'


def check_java(jdk_path):
    if jdk_path is None:
        p = subprocess.Popen('java -version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen('"' + jdk_path + '\\bin\\java" -version', shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    line = str(p.stdout.readline())
    if 'version' in line:
        return line.replace('b\'java version ', '').replace('\\r\\n\'', '')
    else:
        return None
