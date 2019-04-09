# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author : Li Jixue
# Date : 2017/11/08
# Description: 环境设置
# ------------------------------------------------------------------------------

import subprocess
import os

server_info = {
    '李佶学专用': {
        'release_en': 'test',
        'ip': '192.168.60.169',
        'port': 22,
        'username': 'honor',
        'password': 'xx'
    },
    '日文': {
        'release_en': 'jp',
        'ip': '118.24.178.15',
        'port': 4399,
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '韩文': {
        'release_en': 'kr',
        'ip': '118.24.177.74',
        'port': 4399,
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    },
    '内网': {
        'release_en': 'dev',
        'ip': '192.168.20.246',
        'port': 22,
        'fight_ip': '192.168.20.246',
        'username': 'honor',
        'password': 'zK2p@dM$bh'
    }
}

paths = {

}

lock = None


remote_root_path = '/home/honor/online/'
work_path = os.path.expanduser('~') + '\\CL_Srv_Pub_Tool'
work_config_path = work_path + '\\config'
work_history_path = work_path + '\\history'
work_lock_path = work_path + '\\lock'
env_user_name=''
work_config_release = 'release'
work_config_srv_type = 'srv_type'
work_config_maven_path = 'maven_path'
work_config_upload_csv = 'upload_csv'
work_config_save_path = 'save_path'
work_config_paths = 'paths'
work_config_log_file = os.path.expanduser('~') + '\\Desktop\\build.log'
work_config_user_name = 'user_name'


# 检查jdk路径
def check_java(jdk_path):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if jdk_path is None:
        cmd = 'java -version'
    else:
        cmd = '"' + jdk_path + '\\bin\\java" -version'
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         startupinfo=si, env=os.environ.copy())
    line = str(p.stdout.readline())
    if 'version' in line:
        return line.replace('b\'java version ', '').replace('\\r\\n\'', '')
    else:
        return None


# 检查maven路径
def check_maven(maven_path):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = '"' + maven_path + '\\bin\\mvn.bat" -v'
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         startupinfo=si)
    res = ''
    # Apache Maven 3.2.5 (12a6b3acb947671f09b81f49094c53f426d8cea1; 2014-12-15T01:29:23+08:00)
    # Maven home: E:\develop\apache-maven-3.2.5\bin\..
    # Java version: 1.6.0_45, vendor: Sun Microsystems Inc.
    # Java home: E:\develop\jdk1.6.0_45\jre
    # Default locale: zh_CN, platform encoding: GBK
    # OS name: "windows 7", version: "6.1", arch: "amd64", family: "windows"
    line = str(p.stdout.readline())
    while line != 'b\'\'':
        if line.find('Apache Maven') >= 0:
            maven_ver = line[line.index('Apache Maven') + 13:line.index('(') - 1].replace('b\'', '')
            if maven_ver != '3.2.5':
                raise Exception("错误：只能选择3.2.5版本的Maven")
            res += 'Maven版本：' + maven_ver + '\n'
        elif line.find('Java version') >= 0:
            java_ver = line[line.index(':') + 2:line.index(',')].replace('b\'', '')
            if '1.6' not in java_ver:
                raise Exception("错误：请将1.6版本的Jdk添加到环境变量：JAVA_HOME")
            res += 'JDK版本：' + java_ver + '\n'
        elif line.find('UnsupportedClassVersionError') >= 0:
            raise Exception("错误：只能选择3.2.5版本的Maven")
        line = str(p.stdout.readline())
    return res
